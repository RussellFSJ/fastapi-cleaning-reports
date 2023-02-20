from typing import Optional
from pydantic import BaseModel, Field
from models.object_id import PydanticObjectId


class CleaningReportModel(BaseModel):
    id: PydanticObjectId = Field(alias="_id")
    robot_id: str
    building_name: str
    location_name: str
    cleaning_status: str
    cleaning_zone_percentage: float
    coverage_percentage: float
    cleaning_productivity: float
    percentage_of_max_cleaning_productivity: float
    battery_usage: int
    date: str
    start_time: str
    end_time: str
    cleaning_duration: str
    total_area: float
    cleanable_area: float
    cleaning_zones_area: float
    cleaned_area: float
    missed_cleaning_area: float
    cleaning_zones_img_url: Optional[str]
    cleaned_area_img_url: Optional[str]
    cleaning_zones_w_cleaned_img_url: Optional[str]
    missed_area_img_url: Optional[str]
    complete_img_url: Optional[str]


class MinCleaningReportModel(BaseModel):
    id: PydanticObjectId = Field(alias="_id")
    robot_id: str
    building_name: str
    location_name: str
    date: str
    start_time: str
    end_time: str


class UpdateCleaningReportModel(BaseModel):
    robot_id: Optional[str]
    building_name: Optional[str]
    location_name: Optional[str]
    cleaning_status: Optional[str]
    cleaning_zone_percentage: Optional[float]
    coverage_percentage: Optional[float]
    cleaning_productivity: Optional[float]
    percentage_of_max_cleaning_productivity: Optional[float]
    battery_usage: Optional[int]
    date: Optional[str]
    start_time: Optional[str]
    end_time: Optional[str]
    cleaning_duration: Optional[str]
    total_area: Optional[float]
    cleanable_area: Optional[float]
    cleaning_zones_area: Optional[float]
    cleaned_area: Optional[float]
    missed_cleaning_area: Optional[float]
    cleaning_zones_img_url: Optional[str]
    cleaned_area_img_url: Optional[str]
    cleaning_zones_w_cleaned_img_url: Optional[str]
    missed_area_img_url: Optional[str]
    complete_img_url: Optional[str]
