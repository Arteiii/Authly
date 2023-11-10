from bson import ObjectId


def convert_object_id_to_str(data):
    """
    Convert ObjectId to string in a dictionary and rename _id to id.
    """
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, dict):
                convert_object_id_to_str(value)
            elif isinstance(value, ObjectId):
                data[key] = str(value)
        if "_id" in data:
            data["id"] = data.pop("_id")
    return data


def convert_str_to_object_id(data):
    """
    Convert the 'id' string back into the '_id' ObjectId type.
    """
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, dict):
                convert_str_to_object_id(value)
            elif key == "id":
                data["_id"] = ObjectId(value)
                del data["id"]
    return data
