import os
import motor.motor_asyncio
from models import cleaning_reports


client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["DATABASE_URL"])
database = client.remote_management
collection = database.cleaning_reports


async def update_cleaning_report(id, cleaning_zones_img_url):
    await collection.update_one(
        {"_id": id}, {"$set": {"cleaning_zones_img_url": cleaning_zones_img_url}}
    )
    document = await collection.find_one({"_id": id})
    return document


async def delete_cleaning_report(id):
    await collection.delete_one({"_id": id})
    return True
