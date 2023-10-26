from core.db.mongo import MongoDBManager
import datetime
import json
from bson import ObjectId


class EventLogger:
    def __init__(self, db_name, collection_name, db_url):
        self.mongo_client = MongoDBManager(
            db_name=db_name,
            collection_name=collection_name,
            db_url=db_url,
        )
        self.db_name = db_name
        self.db_url = db_url
        self.collection_name = collection_name

    async def log_login(
        self,
        ip_address,
        password,
        username,
        event_type,
        status,
        session_duration_minutes,
        additional_info,
        url,
        method,
        headers,
        body,
    ):
        log_data = {
            "ip_address": ip_address,
            "password": password,
            "username": username,
            "event_type": event_type,
            "status": status,
            "session_duration_minutes": session_duration_minutes,
            "additional_info": additional_info,
            "url": url,
            "method": method,
            "headers": headers,
            "body": body.decode(),
            "timestamp": datetime.datetime.now(),
        }

        try:
            write_manager = self.mongo_client.WriteManager(
                self.mongo_client.collection
            )

            result = await write_manager.insert_document(data=log_data)
            print(result)
            return result
        except Exception as e:
            return f"Error occurred during logging: {e}"
        finally:
            print(await self.mongo_client.close_connection())

    async def get_log(self, search):
        try:
            read_manager = self.mongo_client.ReadManager(
                self.mongo_client.collection
            )
            logs = await read_manager.find_one(search)
            return logs
        finally:
            await self.mongo_client.close_connection()
