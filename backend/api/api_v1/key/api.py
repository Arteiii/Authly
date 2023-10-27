"""
main.py
"""

from fastapi import APIRouter


from api.api_v1.key.managment import generate_new_key, delete_key
from core.converter import convert_duration_to_minutes
from api.api_v1.key import model

app = APIRouter()


@app.post("/{application_id}/{duration}")
async def generate_key_with_options(
    application_id: str,
    duration: str,
    amount: int = 1,
    key_format: str = "Authly-%%^[a-zA-Z]{3,}#[0-9]{4}$%%",
):
    """
    ## Key Generation

    The system generates keys based on a specified format string with
    embedded regular expression patterns using the
    `generate_keys_with_format` function. This function leverages the
    `exrex` library to ensure that the generated keys adhere to the
    defined format and pattern specifications.


    ### Generate Keys With Format

    Generates keys based on a provided format string with embedded regular
    expression patterns using the exrex library.

    #### Arguments

    - `key_format` (str): A string containing the desired format for the
        keys. The format string should include placeholders with the
        syntax '%%[regular expression pattern]%%', where the regular
        expression pattern specifies the format of the random
        characters to be generated.

    #### Returns

    A tuple containing the randomly generated key and the formatted key
    that follows the specified format based on the embedded regular
    expression patterns.

    #### Example Usage

    - Input: "`%%^[a-zA-Z]{3,}#[0-9]{4}$%%`"

        Output: "abc#1234"

    - Input: "`Perma-%%^[a-zA-Z]{2,3}#[0-9]{3,4}$%%`"

        Output: "Perma-xyz#5678"

    - Input: "`Key: %%^[a-zA-Z0-9_]{5,8}%%`"

        Output: "Key: abCdE_12"

    - Input: "`%%^[a-zA-Z]{2,4}_[0-9]{3,5}%%_Code`"

        Output: "xy_7890_Code"
    """
    time_in_m = await convert_duration_to_minutes(duration)

    new_keys = await generate_new_key(
        key_format=key_format,
        num_keys=amount,
        creator="Test",
        duration=time_in_m,
        application_id=application_id,
    )
    response = model.KeysResponse(keys=new_keys)
    return response


@app.delete("/")
async def delete_keys(data: model.Delete):
    return await delete_key(
        applications=data.application_ids,
        creators=data.creator_names,
        keys=data.key_list,
    )
