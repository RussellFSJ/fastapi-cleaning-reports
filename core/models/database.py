import os
import motor.motor_asyncio
from core.schemas import cleaningReports


client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["DATABASE_URL"])
database = client.remote_management
collection = database.cleaning_reports


async def fetch_one_cleaning_report(id):
    document = await collection.find_one({"_id": id})
    return document


async def fetch_all_cleaning_reports():
    cleaning_reports = []
    cursor = collection.find({})
    async for document in cursor:
        cleaning_reports.append(cleaningReports.CleaningReport(**document))
    return cleaning_reports


async def create_cleaning_report(cleaning_report):
    document = cleaning_report
    result = await collection.insert_one(document)
    return document


async def update_cleaning_report(id, cleaning_zones_img_url):
    await collection.update_one({"_id": id}, {"$set": {"cleaning_zones_img_url": cleaning_zones_img_url}})
    document = await collection.find_one({"_id": id})
    return document


async def delete_cleaning_report(id):
    await collection.delete_one({"_id": id})
    return True
