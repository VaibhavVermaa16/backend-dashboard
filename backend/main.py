from typing import Dict, List, Union
import uvicorn
from fastapi import FastAPI, Query
from fastapi import APIRouter
from services.user_profile_analytics import analyse_user, fetch_data_by_time_slot, get_chat_history, list_users
from services.call_analytics import call_details
from services.business_analytics import get_all_business_names, get_business_details_by_name, business_analytics_by_state
from services.entrepreneur_analytics import list_entrepreneur,get_entrepreneur_details_by_name, entrepreneur_analytics_by_state
from services.waitlist_analytics import get_waiting_persons
from bson.json_util import dumps
import json
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="Chat Analyzer Dashboard", root_path="/api/v1")

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

router = APIRouter()

@app.get("/")
async def root():
    return {"message": "Welcome to Chat Analyzer Dashboard"}

@app.post("/analyse")
def chats(user: dict):
    data = analyse_user(user)
    return json.loads(dumps(data))

@app.post("/chathistory")
def chat_history(user: dict):
    return get_chat_history(user)

@app.get("/users")
def get_all_users():
    return list_users()

@app.post("/call")
def get_call_details(user: dict):
    return call_details(user)

@app.get("/all/business")
def list_all_business():
    return get_all_business_names()

@app.post("/business")
def get_business_data(name: dict):
    return get_business_details_by_name(name)

@app.post("/business/state")
def get_business_by_city(city: dict):
    return business_analytics_by_state(city)

@app.get("/all/entrepreneur")
def list_all_entrepreneur():
    return list_entrepreneur()

@app.post("/entrepreneur")
def get_entrepreneur_data(name: dict):
    return get_entrepreneur_details_by_name(name)

@app.post("/entrepreneur/state")
def get_entrepreneur_by_city(city: dict):
    return entrepreneur_analytics_by_state(city)

@app.get("/all/waiting")
def get_waiting_list():
    return get_waiting_persons()

@app.get("/users-by-time-slot", response_model=Union[List[str], Dict[str, Union[str, int, Dict]]])
async def user_by_time_slot(
    from_time: str = Query(..., description="Start time in format: DD-MM-YYTHH:MM:SS"),
    to_time: str = Query(..., description="End time in format: DD-MM-YYTHH:MM:SS")
):
    return fetch_data_by_time_slot(from_time, to_time)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)