from collections import Counter
from db.collections import business_collection
import json
from bson.json_util import dumps

def get_all_business_names():
    try:
        data = business_collection.find().to_list()
        names=[]
        for business in data:
            if business["name"] and str(business["name"]) != "nan":
                names.append(str(business["name"]))
        return {"Total Registered": len(names) ,"Businesses":names}
    except Exception as e:
        print("Error in get_all_business_names:", e)
        return []
   
 
def get_business_details_by_name(name):
    try:
        data = business_collection.find_one({"name": str(name["name"])})
        if(data):
            return json.loads(dumps(data))
        return {}
    except Exception as e:
        print("Error in get_business_details:", e)
        return {}
    
def business_analytics_by_state(state):
    try:
        if(state["state"]):
            data = business_collection.find({"state": {"$regex": f"^{state["state"]}$", "$options": "i"}}).to_list(None)
            
            data = [business["name"] for business in data]
            count = len(data)
            if count == 0:
                return {"error": "No business found in the given state"}
            
            return {"Total Registered": count ,"Businesses":data}
        
        data = business_collection.find().to_list()
        
        # Filter out businesses with no name
        data = [
                business
                for business in data
                if "name" in business and isinstance(business["name"], str)
            ]
        
        business_data = {}
        for business in data:
            
            if business["state"] and len(business["state"]) > 0:
                
                if business["state"] in business_data:
                    business_data[business["state"]].append(business["name"])
                else:
                    business_data[business["state"]] = [business["name"]]
                    
        # count frequency of each state
        frequency = dict(Counter([business["state"] for business in data]))
        business_data = json.loads(dumps(business_data))

        return {"Total Registered": frequency ,"Businesses":business_data}
    
    except Exception as e:
        print("Error in business_analytics_by_state:", e)
        return {}

