from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


router = APIRouter()


@router.get(
    "/",
    status_code=200,
    response_description="Checks if server is alive",
    tags=["root"],
)
def read_root():
    response = {
        "success": True,
        "message": "Welcome to FastAPI MongoDB Server!",
    }

    return JSONResponse(content=jsonable_encoder(response))
