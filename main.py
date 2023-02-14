import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from core.models.database import *

load_dotenv()

app = FastAPI()

origins = ["http://localhost:8090"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/api/cleaning_reports")
async def get_cleaning_reports():
    pass


@app.get("/api/cleaning_reports{id}")
async def get_cleaning_reports_by_id(id):
    pass


@app.post("/api/cleaning_reports")
async def post_cleaning_reports(report):
    pass


@app.put("/api/cleaning_reports{id}")
async def update_cleaning_reports(id, data):
    pass


@app.delete("/api/cleaning_reports{id}")
async def delete_cleaning_reports(id):
    pass


# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=os.environ["PORT"])
