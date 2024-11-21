import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors

class JobRecommender:
    def __init__(self, employee_features, job_features):
        """
        Initialize KNN Job Recommender
        
        Args:
            employee_features (dict): Employee characteristics
            job_features (list): List of job dictionaries
        """
        self.employee_features = employee_features
        self.job_features = job_features
        
        # Predefined feature order for consistency
        self.feature_order = [
            'job_type_id',
            'position_id', 
            'year_experience', 
            'max_salary', 
            'min_salary', 
            'industry_id', 
            'contract_type_id', 
            'district_id', 
            'city_id'
        ]
    
    def calculate_skill_match(self, job_skills):
        """
        Advanced skill matching calculation
        
        Args:
            job_skills (list): Skills for a specific job
        
        Returns:
            float: Comprehensive skill matching score
        """
        employee_skills = self.employee_features.get('skill_ids', [])
        
        if not employee_skills or not job_skills:
            return 0.0
        
        # Exact skill match
        exact_match = len(set(employee_skills) & set(job_skills))
        
        # Partial skill match calculation
        total_skills = len(set(employee_skills + job_skills))
        partial_match_ratio = exact_match / total_skills
        
        # Weighted skill match
        skill_match_score = (
            0.7 * (exact_match / max(len(employee_skills), 1)) +  # Exact match weight
            0.3 * partial_match_ratio  # Partial match weight
        )
        
        return min(1.0, skill_match_score)
    
    def calculate_salary_compatibility(self, job_salary):
        """
        Comprehensive salary compatibility calculation
        
        Args:
            job_salary (dict): Job salary details
        
        Returns:
            float: Salary compatibility score (0-1)
        """
        # Employee's salary range
        employee_min_salary = self.employee_features.get('min_salary', 0)
        employee_max_salary = self.employee_features.get('max_salary', float('inf'))
        
        # Job's salary range
        job_min_salary = job_salary.get('min_salary', 0)
        job_max_salary = job_salary.get('max_salary', float('inf'))
        
        # Scenario 1: Complete Salary Range Overlap
        if (job_min_salary <= employee_max_salary and 
            job_max_salary >= employee_min_salary):
            
            # Calculate overlap percentage
            overlap_start = max(employee_min_salary, job_min_salary)
            overlap_end = min(employee_max_salary, job_max_salary)
            
            # Total employee salary range
            total_employee_range = employee_max_salary - employee_min_salary
            
            # Overlap range
            overlap_range = max(0, overlap_end - overlap_start)
            
            # Compatibility score based on overlap
            compatibility_score = overlap_range / total_employee_range
            
            return max(0, min(1, compatibility_score))
        
        # Scenario 2: No Overlap
        else:
            # Calculate proximity penalty
            if job_max_salary < employee_min_salary:
                # Job salary is lower than employee's minimum
                proximity_penalty = 1 - (employee_min_salary - job_max_salary) / employee_min_salary
            else:
                # Job salary is higher than employee's maximum
                proximity_penalty = 1 - (job_min_salary - employee_max_salary) / job_min_salary
            
            return max(0, min(1, proximity_penalty * 0.5))  # Reduced penalty
    
    def extract_features(self, item, is_employee=False):
        """
        Enhanced feature extraction with skill and salary compatibility
        
        Args:
            item (dict): Job or employee dictionary
            is_employee (bool): Flag to handle employee-specific logic
        
        Returns:
            list: Feature vector
        """
        features = []
        
        for feature in self.feature_order:
            # Default to 0 if feature not present
            value = item.get(feature, 0.0)
            
            # Special handling for salary features
            if feature in ['max_salary', 'min_salary']:
                if is_employee:
                    # Use employee's salary expectation
                    value = item.get(feature, 0.0)
                else:
                    # Calculate salary compatibility
                    salary_compatibility = self.calculate_salary_compatibility({
                        'min_salary': item.get('min_salary', 0),
                        'max_salary': item.get('max_salary', 0)
                    })
                    value = salary_compatibility
            
            features.append(value)
        
        # Add skill matching feature with advanced calculation
        skill_match = self.calculate_skill_match(item.get('skill_ids', []))
        features.append(skill_match)
        
        return features
    
    def prepare_feature_matrix(self):
        """
        Prepare feature matrix for KNN
        
        Returns:
            tuple: (feature matrix, scaler)
        """
        # Extract features for all jobs
        job_features = [self.extract_features(job) for job in self.job_features]
        
        # Standardize features
        scaler = StandardScaler()
        normalized_features = scaler.fit_transform(job_features)
        
        return normalized_features, scaler
    
    def recommend_jobs(self, k=5):
        """
        Recommend top K jobs using KNN with advanced matching
        
        Args:
            k (int): Number of job recommendations
        
        Returns:
            list: Top K recommended jobs with similarity scores
        """
        # Prepare feature matrix
        job_features_matrix, scaler = self.prepare_feature_matrix()
        
        # Prepare employee feature vector
        employee_vector = self.extract_features(self.employee_features, is_employee=True)
        
        # Normalize employee vector
        normalized_employee = scaler.transform([employee_vector])
        
        # Create KNN model
        knn = NearestNeighbors(n_neighbors=k, metric='euclidean')
        knn.fit(job_features_matrix)
        
        # Find nearest neighbors
        distances, indices = knn.kneighbors(normalized_employee)
        
        # Prepare recommendations
        recommendations = []
        for dist, idx in zip(distances[0], indices[0]):
            job = self.job_features[idx]
            
            # Advanced similarity calculation
            skill_match = self.calculate_skill_match(job.get('skill_ids', []))
            salary_compatibility = self.calculate_salary_compatibility({
                'min_salary': job.get('min_salary', 0),
                'max_salary': job.get('max_salary', 0)
            })
            
            # Convert distance to similarity score
            base_similarity = 1 / (1 + dist)
            
            # Weighted similarity score
            weighted_similarity = (
                0.5 * base_similarity +  # Base KNN similarity
                0.3 * skill_match +      # Skill match weight
                0.2 * salary_compatibility  # Salary compatibility weight
            )
            
            recommendations.append({
                'job': job,
                'similarity_score': float(weighted_similarity),
                'skill_match': float(skill_match),
                'salary_compatibility': float(salary_compatibility),
                'distance': float(dist)
            })
        
        # Sort by weighted similarity score (descending)
        recommendations.sort(key=lambda x: x['similarity_score'], reverse=True)
        
        return recommendations