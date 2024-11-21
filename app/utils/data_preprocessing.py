def clean_numeric_fields(data):
    """
    Clean numeric fields by converting None/null to 0
    Preserves array/list fields completely
    
    Args:
        data (dict or list): Input data to clean
    
    Returns:
        Cleaned data with null numeric values replaced
    """
    def clean_item(item):
        cleaned_item = item.copy()
        
        for key, value in item.items():
            # Skip if value is a list/array
            if isinstance(value, (list, tuple)):
                continue
            
            # Convert None or null to 0 for numeric fields
            if value is None:
                cleaned_item[key] = 0
            
            # Optional: Type conversion for safety
            try:
                cleaned_item[key] = float(cleaned_item[key])
            except (ValueError, TypeError):
                pass
        
        return cleaned_item
    
    # Handle list or single dictionary input
    if isinstance(data, list):
        return [clean_item(item) for item in data]
    elif isinstance(data, dict):
        return clean_item(data)
    else:
        raise ValueError("Input must be a dictionary or list of dictionaries")