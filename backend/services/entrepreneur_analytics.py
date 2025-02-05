from collections import Counter
from db.collections import entrepreneur_collection
import json
from bson.json_util import dumps

def list_entrepreneur():
    try:
        data = entrepreneur_collection.find().to_list()
        names=[]
        for entrepreneur in data:
            if entrepreneur["name"] and str(entrepreneur["name"]) != "nan":
                names.append(str(entrepreneur["name"]))
        return {"Total Registered": len(names) ,"Entrepreneurs":names}
    except Exception as e:
        print("Error in list_entrepreneur:", e)
        return []

def get_entrepreneur_details_by_name(name):
    try:
        data = entrepreneur_collection.find_one({"name": str(name["name"])})
        if(data):
            return json.loads(dumps(data))
        
        return {}
        
    except Exception as e:
        print("Error in get_entrepreneur_details:", e)
        return {}    

def entrepreneur_analytics_by_state(state):
    try:
        if "current_state" in state: 
            data = entrepreneur_collection.find(
                {"current_state": {"$regex": f"^{state['state']}$", "$options": "i"}}
            ).to_list(None)

            # Filter out documents without a valid 'name'
            data = [
                entrepreneur["name"]
                for entrepreneur in data
                if "name" in entrepreneur and isinstance(entrepreneur["name"], str)
            ]
            count = len(data)
            if count == 0:
                return {"error": "No entrepreneur(s) found in the given state"}

            return {"Total Registered": count, "Entrepreneurs": data}

        # Fetch all data if 'current_state' is not provided
        data = entrepreneur_collection.find().to_list(None)

        # Filter out documents without a valid 'name'
        data = [
            entrepreneur
            for entrepreneur in data
            if "name" in entrepreneur and isinstance(entrepreneur["name"], str)
        ]

        entrepreneur_data = {}
        for entrepreneur in data:
            # Check if 'current_state' exists and is valid
            if "current_state" in entrepreneur and entrepreneur["current_state"]:
                current_state = entrepreneur["current_state"]

                if current_state in entrepreneur_data:
                    entrepreneur_data[current_state].append(entrepreneur["name"])
                else:
                    entrepreneur_data[current_state] = [entrepreneur["name"]]

        # Count frequency of each state
        frequency = dict(
            Counter(
                [
                    entrepreneur["current_state"]
                    for entrepreneur in data
                    if "current_state" in entrepreneur and entrepreneur["current_state"]
                ]
            )
        )
        entrepreneur_data = json.loads(dumps(entrepreneur_data))

        return {"Total Registered": frequency, "Entrepreneurs": entrepreneur_data}

    except Exception as e:
        print("Error in entrepreneur_analytics_by_state:", e)
        return {}
