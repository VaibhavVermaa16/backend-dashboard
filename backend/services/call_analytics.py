from db.collections import call_logs_collection as collection
from db.collections import user_collection 

def count_successful_calls(item):
    try:
        if isinstance(item, dict):
            item = [item]
        # Check if the field exists and is greater than 0
        count=0
        for data in item:
            if "status" in data and data["status"] == "completed":
                count+= 1
        return count
    except Exception as e:
        print("Error in count_successful_calls:", e)
        return 0

def total_calls_made(item):
    try:
        if isinstance(item, dict):
            item = [item]
        # Check if the field exists and is greater than 0
        count=0
        for data in item:
            if "status" in data:
                count+= 1
        return count
    except Exception as e:
        print("Error in total_calls_made:", e)
        return 0

def call_details(user):
    try:
        if "user" not in user:
            user["user"] = "all"
            
        #get user data from post request
        data = collection.find().to_list()
        if(user["user"]!= "all"):
            number = user_collection.find_one({"whatsapp_username": user["user"]}).get("phone_number")
            data = [caller for caller in data if caller["caller_number"] == str(number)]
            
        success=count_successful_calls(data)
        total=total_calls_made(data)
        return {
            "Successful_calls":success, "Total calls":total, 
            "Call_connection_rate": str((success/total).__round__(2) * 100)+"%"
        }
        # return json.loads(dumps(data))
    except Exception as e:
        print("Error in get_call_details:", e)
        return []