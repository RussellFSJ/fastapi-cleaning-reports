from models.object_id import PydanticObjectId
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Body, Request, status
from models.cleaning_reports import (
    CleaningReportModel,
    MinCleaningReportModel,
    UpdateCleaningReportModel,
)

router = APIRouter()


@router.get(
    "/",
    status_code=200,
    response_description="Get all cleaning reports",
    tags=["cleaning_report"],
)
async def get_all_cleaning_reports(request: Request):
    success = False
    message = "Failed to retrieve cleaning report(s)."

    cleaning_reports = []

    try:
        # only getting the fields below as collection may be really big
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
            try:
                # validates each document against MinCleaningReportModel
                cleaning_reports.append(MinCleaningReportModel(**document))

                message = "No cleaning report(s) found."

                if len(cleaning_reports) != 0:
                    message = "Successfully retrieved cleaning report(s)."

                success = True

            except Exception as error:
                id = document["_id"]
                message += f" Please check document id {id}. {error}"

    except Exception as error:
        message += f" {error}"

    response = {
        "success": success,
        "message": message,
        "cleaning_reports": cleaning_reports,
    }

    return JSONResponse(
        status_code=status.HTTP_200_OK, content=jsonable_encoder(response)
    )


@router.get(
    "/{id}",
    status_code=200,
    response_description="Get cleaning report by ID",
    tags=["cleaning_report"],
)
async def get_cleaning_report_by_id(request: Request, id: PydanticObjectId):
    success = False
    message = f"Failed to retrieve cleaning report {id}."

    cleaning_report = {}

    try:
        message = "No cleaning report found."

        cleaning_report = await request.app.mongodb["cleaning_reports"].find_one(
            {"_id": id}
        )

        if cleaning_report != None:
            # validate document against CleaningReportModel
            cleaning_report = CleaningReportModel(**cleaning_report)
            message = f"Successfully retrieved cleaning report {id}."

        success = True

    except Exception as error:
        message += f" {error}"

    response = {
        "success": success,
        "message": message,
        "cleaning_report": cleaning_report,
    }

    return JSONResponse(
        status_code=status.HTTP_200_OK, content=jsonable_encoder(response)
    )


@router.post(
    "/",
    status_code=201,
    response_description="Create cleaning report",
    tags=["cleaning_report"],
)
async def create_cleaning_report(
    request: Request, cleaning_report: UpdateCleaningReportModel = Body(...)
):
    success = False
    message = f"Failed to create cleaning report."

    document = jsonable_encoder(cleaning_report)

    try:
        # _id is automatically inserted if not provided
        new_document = await request.app.mongodb["cleaning_reports"].insert_one(
            document
        )

        if new_document:
            message = "Successfully created cleaning report."

        # query document in collection to get document with _id
        created_document = await request.app.mongodb["cleaning_reports"].find_one(
            {"_id": new_document.inserted_id}
        )

        # validate document against CleaningReportModel
        created_document = CleaningReportModel(**created_document)

        success = True

    except Exception as error:
        message += f" {error}"

    response = {
        "success": success,
        "message": message,
        "cleaning_report": created_document,
    }

    return JSONResponse(
        status_code=status.HTTP_201_CREATED, content=jsonable_encoder(response)
    )


@router.put(
    "/{id}",
    status_code=201,
    response_description="Update cleaning report",
    tags=["cleaning_report"],
)
async def update_cleaning_report(
    request: Request,
    id: PydanticObjectId,
    cleaning_report: UpdateCleaningReportModel = Body(...),
):
    success = False
    message = f"Failed to update cleaning report."

    document = jsonable_encoder(cleaning_report)

    try:
        # _id is automatically inserted if not provided
        new_document = await request.app.mongodb["cleaning_reports"].update_one(
            document
        )

        if new_document:
            message = "Successfully updated cleaning report."

        # query document in collection to get document with _id
        updated_document = await request.app.mongodb["cleaning_reports"].find_one(
            {"_id": id}
        )

        # validate document against CleaningReportModel
        updated_document = CleaningReportModel(**updated_document)

        success = True

    except Exception as error:
        message += f" {error}"

    response = {
        "success": success,
        "message": message,
        "cleaning_report": updated_document,
    }

    return JSONResponse(
        status_code=status.HTTP_201_CREATED, content=jsonable_encoder(response)
    )


@router.delete("/api/cleaning_reports{id}")
async def delete_cleaning_reports(id):
    pass
