from flask import Blueprint, abort, app, jsonify, request
from app.utils.job_recommender import JobRecommender


recommend_bp = Blueprint('recommend', __name__)

def safe_get(obj, *keys, default=0):
    """
    Safely navigate nested dictionaries, handling None values
    
    Args:
        obj (dict/None): Starting object
        *keys: Path of keys to navigate
        default: Default value if path cannot be resolved
    
    Returns:
        Value at the nested key path or default
    """
    try:
        for key in keys:
            if obj is None:
                return default
            obj = obj.get(key, {})
        return obj if obj != {} else default
    except Exception:
        return default

def remove_none_values(d):
    """
    Recursively remove keys with None values from a dictionary
    
    Args:
        d (dict): Input dictionary
    
    Returns:
        dict: Dictionary with None values removed
    """
    if not isinstance(d, dict):
        return d
    
    return {
        k: remove_none_values(v) 
        for k, v in d.items() 
        if v is not None and 
           (not isinstance(v, (list, dict)) or len(v) > 0)
    }

def flatten_job_data(jobs):
    """
    Flatten job data with robust error handling and remove None values
    
    Args:
        jobs (list): List of job dictionaries
    
    Returns:
        list: Flattened job dictionaries
    """
    flattened_jobs = []
    
    for job in jobs:
        if job is None:
            continue  # Skip None entries
        
        flattened_job = remove_none_values({
            'id': job.get('id'),
            'job_type_id': safe_get(job, 'jobType', 'id'),
            'position_id': safe_get(job, 'position', 'id'),
            'year_experience': safe_get(job, 'yearExperience'),
            'max_salary': safe_get(job, 'maxSalary'),
            'min_salary': safe_get(job, 'minSalary'),
            'industry_id': safe_get(job, 'industry', 'id'),
            'contract_type_id': safe_get(job, 'contractType', 'id'),
            'district_id': safe_get(job, 'district', 'id'),
            'city_id': safe_get(job, 'city', 'id'),
            'skill_ids': [skill_id for skill_id in job['skill_ids'] if skill_id is not None] if job.get('skill_ids') else []
        })
        
        if flattened_job:  # Only append non-empty dictionaries
            flattened_jobs.append(flattened_job)
    
    return flattened_jobs

def flatten_employee_data(employee):
    """
    Flatten employee data and remove None values
    
    Args:
        employee (dict): Employee dictionary
    
    Returns:
        dict: Flattened employee dictionary
    """
    career_goal = employee.get('careerGoal', {}) or {}
    
    flattened_employee = remove_none_values({
        'education_level_ids': employee.get('educationLevelIds', []),
        'industry_id': safe_get(career_goal, 'industryId') or safe_get(employee, 'industry', 'id'),
        'job_type_id': safe_get(career_goal, 'jobTypeId') or safe_get(employee, 'jobType', 'id'),
        'min_salary': safe_get(career_goal, 'minSalary') or employee.get('minSalary'),
        'max_salary': safe_get(career_goal, 'maxSalary') or employee.get('maxSalary'),
        'position_id': safe_get(career_goal, 'positionId') or safe_get(employee, 'position', 'id'),
        'skill_ids': employee.get('skillIds', [])
    })
    
    return flattened_employee

@recommend_bp.route('/recommend', methods=['POST'])
def demonstrate_job_recommendation():
    try:
        data = request.get_json()
        
        if not data or 'jobs' not in data or 'employee' not in data:
            return jsonify({'error': 'Invalid input'}), 400
        
        recommender = JobRecommender(
            flatten_employee_data(data['employee']), 
            flatten_job_data(data['jobs'])
        )

        # print(flatten_employee_data(data['employee']))
        # print(flatten_job_data(data['jobs']))
        
        recommended_jobs = recommender.recommend_jobs(k=4)
        
        job_list_ids = []
        for rec in recommended_jobs:
            job_list_ids.append({
                'jobId' : rec['job']['id'],
                'similarityScore' : rec['similarity_score']
            })
            
            print(f"Similarity Score: {rec['similarity_score']:.2f}\n")
        return jsonify(job_list_ids), 200;
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'error': str(e)}), 200
    
@recommend_bp.route('/similar', methods=['POST'])
def get_similar_jobs():
    try:
        data = request.get_json()
        
        if not data or 'jobs' not in data or 'jobId' not in data:
            return jsonify({'error': 'Invalid input'}), 400
        
        recommender = JobRecommender(
            {},
            flatten_job_data(data['jobs'])
        )

        print('/similar')
        print(flatten_job_data(data['jobs']))
        
        similar_jobs = recommender.recommend_similar_jobs(
            job_id=data['jobId'], 
            k=5
        )
        
        job_list_ids = []
        for rec in similar_jobs:
            job_list_ids.append({
                'jobId': rec['job']['id'],
                'similarityScore': rec['similarity_score']
            })
            print(f"Similarity Score: {rec['similarity_score']:.2f}\n")
        
        return jsonify(job_list_ids), 200
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'error': str(e)}), 400