from bson import ObjectId
from typing import Any, Union


def convert_object_id_to_str_dictionary(
    data: Union[dict, Any]
) -> Union[dict, Any]:
    """
    Convert ObjectId to string in a dictionary and rename _id to id.
    """
    if data is None:
        return None

    if isinstance(data, dict):
        for key, value in data.items():
            data[key] = convert_object_id_to_str_dictionary(value)
            if isinstance(value, ObjectId):
                data[key] = str(value)
        if "_id" in data:
            data["id"] = data.pop("_id")
    return data


def convert_object_id_to_string(object_id):
    """
    Convert single ObjectId to string
    """
    if isinstance(object_id, ObjectId):
        return str(object_id)
    else:
        # If it's not an ObjectId, return it as is (it might already be a string)
        return object_id


def convert_str_to_object_id(data: Union[dict, Any]) -> Union[dict, Any]:
    """
    Convert the 'id' string back into the '_id' ObjectId type.
    """
    if isinstance(data, dict):
        # Create a copy of the dictionary
        data_copy = data.copy()

        for key, value in data.items():
            data_copy[key] = convert_str_to_object_id(value)
            if key == "id":
                data_copy["_id"] = ObjectId(value)
                del data_copy["id"]

        return data_copy

    return data
