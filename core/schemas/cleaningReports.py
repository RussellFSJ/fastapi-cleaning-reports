from pydantic import BaseModel
from bson.objectid import ObjectId


class CleaningReport(BaseModel):
    _id: ObjectId
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
    cleaning_zones_img_url: str
    cleaned_area_img_url: str
    cleaning_zones_w_cleaned_img_url: str
    missed_area_img_url: str
    complete_img_url: str
