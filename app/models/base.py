from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer

class CustomBase:
    """
    Custom base class for SQLAlchemy models with advanced serialization
    """
    # Universal ID primary key
    id = Column(Integer, primary_key=True)

    def as_dict(self, include_fields=None, ignore_nested=None):
        """
        Convert model instance to a dictionary with flexible serialization
        
        :param include_fields: List of specific fields to include
        :param ignore_nested: List of nested objects to ignore
        :return: Dictionary representation of the object
        """
        # Default to empty list if None
        ignore_nested = ignore_nested or []
        
        result = {}

        # Determine fields to serialize
        if include_fields is None:
            # Use all columns if no specific fields are provided
            columns = self.__table__.columns
            include_fields = [column.name for column in columns]

        # Populate result with specified fields
        for field in include_fields:
            # Check if the field exists as a column or relationship
            if hasattr(self, field):
                value = getattr(self, field)
                
                # Handle relationship fields
                if hasattr(self.__mapper__.relationships, field):
                    if value is not None:
                        # Check if this nested object should be ignored
                        if field in ignore_nested:
                            continue
                        
                        # Handle single object relationship
                        if hasattr(value, 'as_dict'):
                            # Recursively serialize with same ignore_nested
                            result[field] = value.as_dict(
                                ignore_nested=ignore_nested
                            )
                        
                        # Handle list of objects
                        elif isinstance(value, list):
                            # Filter out ignored nested objects and serialize
                            result[field] = [
                                obj.as_dict(ignore_nested=ignore_nested) 
                                if hasattr(obj, 'as_dict') 
                                else str(obj) 
                                for obj in value
                            ]
                        else:
                            result[field] = str(value)
                else:
                    # Handle direct attributes
                    result[field] = value

        return result

# Create base using our CustomBase
Base = declarative_base(cls=CustomBase)