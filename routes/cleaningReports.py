from bson.objectid import ObjectId
from fastapi import APIRouter, Request
from models.cleaningReports import CleaningReport

router = APIRouter()


@router.get("/", tags=["cleaning_report"])
async def get_all_cleaning_reports(request: Request):
    success = False
    message = "Failed to retrieve cleaning report(s)."

    cleaning_reports = []

    try:
        cursor = request.app.mongodb["cleaning_reports"].find(
            {},
            {
                "id": 1,
                "robot_id": 1,
                "building_name": 1,
                "location_name": 1,
                "date": 1,
                "start_time": 1,
                "end_time": 1,
            },
        )
        async for document in cursor:
            # to validate fields using CleaningReport schema
            # cleaning_reports.append(CleaningReport(**document))

            # not validating all fields in schema because it takes too long
            cleaning_reports.append(document)

        success = True
        message = "No cleaning report(s) found."

        if len(cleaning_reports) != 0:
            message = "Successfully retrieved cleaning report(s)."
    except Exception as error:
        message += f" {error}"

    response = {
        "success": success,
        "message": message,
        "cleaning_reports": cleaning_reports,
    }

    return response


@router.get("/{id}", tags=["cleaning_report"])
async def get_cleaning_report_by_id(request: Request, id: str):
    success = False
    message = f"Failed to retrieve cleaning report {id}."

    cleaning_report = {}

    try:
        cleaning_report = await request.app.mongodb["cleaning_reports"].find_one(
            {"_id": ObjectId(id)}
        )

        success = True
        message = "No cleaning report found."

        if cleaning_report != None:
            message = f"Successfully retrieved cleaning report {id}."
    except Exception as error:
        message += f" {error}"

    response = {
        "success": success,
        "message": message,
        "cleaning_report": cleaning_report,
    }

    return response


@router.post("/api/cleaning_reports")
async def create_cleaning_reports(request: Request):
    success = False
    message = f"Failed to create cleaning report."

    cleaning_report = {}

    try:
        success = True
        message = "Successfully created cleaning report."
    except Exception as error:
        pass

    response = {
        "success": success,
        "message": message,
        "cleaning_report": cleaning_report,
    }

    return response


@router.put("/api/cleaning_reports{id}")
async def update_cleaning_reports(id, data):
    pass


@router.delete("/api/cleaning_reports{id}")
async def delete_cleaning_reports(id):
    pass
