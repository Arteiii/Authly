from fastapi import HTTPException

from authly.models import admin_crud_model
from authly.interface import admin
from authly.core.utils import hashing


async def create_admin_account(
    new_admin_account: admin_crud_model.CreateAdmin,
):
    new_admin = admin_crud_model.AdminAccount(
        username=new_admin_account.email.split("@")[0],
        password=hashing.get_password_hash(new_admin_account.password),
        email=new_admin_account.email,
        container=[],
        settings=[],
    )

    admin.insert_admin_user()

    # TODO: add logic


async def get_admin_accounts():
    pass
    # TODO: add logic


async def update_admin_account(
    user_id: str, updated_admin_account: admin_crud_model.AdminAccount
):
    # TODO: add logic to update_admin_account

    # for i, admin_account in enumerate(admin_accounts):
    #     if admin_account.username == username:
    #         admin_accounts[i] = updated_admin_account
    #         return updated_admin_account
    raise HTTPException(status_code=404, detail="Admin account not found")


async def delete_admin_account(user_id: str):
    # TODO: add logic

    # for i, admin_account in enumerate(admin_accounts):
    #     if admin_account.username == username:
    #         del admin_accounts[i]
    #         return {"message": "Admin account deleted"}

    raise HTTPException(status_code=404, detail="Admin account not found")


async def get_admin_account_by_id(user_id: str):
    # TODO: add logic
    # for admin_account in admin_accounts:
    #     if admin_account.username == username:
    #         return admin_account
    raise HTTPException(status_code=404, detail="Admin account not found")


async def get_admin_account_by_name(user_id: str):
    # TODO: add logic
    # for admin_account in admin_accounts:
    #     if admin_account.username == username:
    #         return admin_account
    raise HTTPException(status_code=404, detail="Admin account not found")
