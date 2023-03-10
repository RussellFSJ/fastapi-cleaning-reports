from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Body, Request, status
from models.object_id import PydanticObjectId
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

            except Exception as error:
                id = document["_id"]
                message += f" Please check document id {id}. {error}"

        if len(cleaning_reports) != 0:
            message = "Successfully retrieved cleaning report(s)."

        success = True

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
async def get_cleaning_report_by_id(request: Request, id: str):
    success = False
    message = f"Failed to retrieve cleaning report {id}."

    cleaning_report = {}

    try:
        message = "No cleaning report found."

        # query document in collection with given _id
        cleaning_report = await request.app.mongodb["cleaning_reports"].find_one(
            {"_id": PydanticObjectId(id)}
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
    message = "Failed to create cleaning report."

    document = jsonable_encoder(cleaning_report)
    created_document = {}

    try:
        # _id is automatically inserted if not provided
        new_document = await request.app.mongodb["cleaning_reports"].insert_one(
            document
        )

        # query document in collection with given _id
        created_document = await request.app.mongodb["cleaning_reports"].find_one(
            {"_id": new_document.inserted_id}
        )

        # validate document against CleaningReportModel
        created_document = CleaningReportModel(**created_document)

        success = True
        message = "Successfully created cleaning report."

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
    id: str,
    cleaning_report: UpdateCleaningReportModel = Body(...),
):
    success = False
    message = f"Failed to update cleaning report {id}."

    document = {k: v for k, v in cleaning_report.dict().items() if v is not None}
    updated_document = {}

    if len(document) >= 1:
        try:
            new_document = await request.app.mongodb["cleaning_reports"].update_one(
                {"_id": PydanticObjectId(id)}, {"$set": document}
            )

            # checks if document matched for this update
            if new_document.matched_count != 1:
                raise Exception(f"Cleaning report {id} does not exist.")

            # query document in collection to get document with _id
            updated_document = await request.app.mongodb["cleaning_reports"].find_one(
                {"_id": PydanticObjectId(id)}
            )

            # validate document against CleaningReportModel
            updated_document = CleaningReportModel(**updated_document)

            success = True
            message = f"Successfully updated cleaning report {id}."

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


@router.put(
    "/",
    status_code=201,
    response_description="Update cleaning reports",
    tags=["cleaning_report"],
)
async def update_cleaning_reports(
    request: Request,
    query: UpdateCleaningReportModel = Body(...),
    cleaning_report: UpdateCleaningReportModel = Body(...),
):
    success = False
    message = f"Failed to update cleaning report(s)."

    query = {k: v for k, v in query.dict().items() if v is not None}
    document = {k: v for k, v in cleaning_report.dict().items() if v is not None}
    updated_documents = []

    # list of id(s) belonging to reports(s) matching the query
    ids = [
        report["_id"]
        async for report in request.app.mongodb["cleaning_reports"].find(query)
    ]

    if len(ids) == 0:
        message = "No cleaning report(s) found."

    if len(ids) != 0 and len(document) >= 1:
        try:
            # update document(s)
            new_documents = await request.app.mongodb["cleaning_reports"].update_many(
                query, {"$set": document}
            )

            # query for updated document(s)
            cursor = request.app.mongodb["cleaning_reports"].find({"_id": {"$in": ids}})

            async for document in cursor:
                try:
                    # validate document against CleaningReportModel
                    updated_documents.append(CleaningReportModel(**document))

                except Exception as error:
                    id = document["_id"]
                    message += f" Please check document id {id}. {error}"

            if new_documents.matched_count == len(updated_documents):
                success = True
                message = (
                    f"Successfully updated {len(updated_documents)} cleaning report(s)."
                )

        except Exception as error:
            message += f" {error}"

    response = {
        "success": success,
        "message": message,
        "cleaning_report": updated_documents,
    }

    return JSONResponse(
        status_code=status.HTTP_201_CREATED, content=jsonable_encoder(response)
    )


@router.delete(
    "/{id}",
    status_code=200,
    response_description="Delete cleaning report",
    tags=["cleaning_report"],
)
async def delete_cleaning_report(request: Request, id: str):
    success = False
    message = f"Failed to delete cleaning report {id}."

    try:
        # delete document in collection with given _id
        delete_result = await request.app.mongodb["cleaning_reports"].delete_one(
            {"_id": PydanticObjectId(id)}
        )

        if delete_result.deleted_count == 1:
            success = True
            message = f"Successfully deleted cleaning report {id}."

    except Exception as error:
        message += f" {error}"

    response = {
        "success": success,
        "message": message,
    }

    return JSONResponse(
        status_code=status.HTTP_200_OK, content=jsonable_encoder(response)
    )


@router.delete(
    "/",
    status_code=200,
    response_description="Delete cleaning reports",
    tags=["cleaning_report"],
)
async def delete_cleaning_reports(
    request: Request,
    query: UpdateCleaningReportModel = Body(...),
):
    success = False
    message = "Failed to delete cleaning reports."

    query = {k: v for k, v in query.dict().items() if v is not None}

    # list of id(s) belonging to reports(s) matching the query
    ids = [
        report["_id"]
        async for report in request.app.mongodb["cleaning_reports"].find(query)
    ]

    if len(ids) == 0:
        message = "No cleaning report(s) found."

    if len(ids) != 0:
        try:
            # delete document(s) in collection matching query
            delete_result = await request.app.mongodb["cleaning_reports"].delete_many(
                query
            )

            # checks if all document(s) matching query are deleted
            if delete_result.deleted_count == len(ids):
                success = True
                message = f"Successfully deleted {delete_result.deleted_count} cleaning report(s)."

        except Exception as error:
            message += f" {error}"

    response = {
        "success": success,
        "message": message,
    }

    return JSONResponse(
        status_code=status.HTTP_201_CREATED, content=jsonable_encoder(response)
    )
