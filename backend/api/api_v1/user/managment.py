from typing import List


class UserManagment:
    async def create_user(username, email, password, role):
        # add source
        user_id = "raondom generated int"
        # check in db to make suire its the only one
        return user_id, username, email, password, role

    async def update_username(user_id: int, new_username):
        # add source
        return new_username

    async def delete_user(user_id: List[int]):
        db_result = "succe.."  # add logic
        results = {user_id: db_result}
        return results

    async def update_user_roles(
        user_id: [int],
        add_roles: List = None,
        remove_roles: List = None,
        set_roles: List = None,
    ):
        results = {}

        op_result = "suc..."  # returns from mongo crud
        # after ops:
        results = {user_id: op_result}
        return results
