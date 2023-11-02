from bson import ObjectId


def convert_object_id_to_str(data):
    """
    Convert ObjectId to string in a dictionary.
    """
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, dict):
                convert_object_id_to_str(
                    value
                )  # Recursively process nested dictionaries
            elif isinstance(value, ObjectId):
                data[key] = str(value)
    return data
