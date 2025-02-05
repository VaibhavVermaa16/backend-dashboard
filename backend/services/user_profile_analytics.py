from datetime import datetime
import json
from db.collections import user_collection as collection
from collections import Counter
import re

def count_free_notify_trial(item):
    try:
        if isinstance(item, dict):
            item = [item]
        # Check if the field exists and is greater than 0
        count=0
        for data in item:
            if "free_notify_trial_done" in data and data["free_notify_trial_done"] > 0:
                count+= data["free_notify_trial_done"]
        return count
    except Exception as e:
        print("Error in count_notify_trial:", e)
        return 0

def count_free_product_discovery(item):
    try:
        if isinstance(item, dict):
            item = [item]
        # Check if the field exists and is greater than 0
        count=0
        for data in item:
            if "free_product_discovery_done" in data and data["free_product_discovery_done"] > 0:
                count+= data["free_product_discovery_done"]
            
        return count
    except Exception as e:
        print("Error in count_product_discovery:", e)
        return 0

def count_free_custom_done(item):
    try:
        if isinstance(item, dict):
            item = [item]
            
        # Check if the field exists and is greater than 0
        count=0
        for data in item:
            if "free_custom_done" in data and data["free_custom_done"] > 0:
                count += data["free_custom_done"]
            
        return count
    except Exception as e:
        print("Error in count_free_custom_done:", e)
        return 0
    
def count_free_professional_discovery_done(item):
    try:
        if isinstance(item, dict):
            item = [item]
        # Check if the field exists and is greater than 0
        count=0
        for data in item:
            if "free_professional_discovery_done" in data and data["free_professional_discovery_done"] > 0:
                count += data["free_professional_discovery_done"]
            
        return count
    except Exception as e:
        print("Error in count_free_professional_discovery_done:", e)
        return 0

def count_free_reservation_done(item):
    try:
        if isinstance(item, dict):
            item = [item]
        # Check if the field exists and is greater than 0
        count=0
        for data in item:
            if "free_reservation_done" in data and data["free_reservation_done"] > 0:
                count += data["free_reservation_done"]
            
        return count
    except Exception as e:
        print("Error in count_free_reservation_done:", e)
        return 0

def count_number_of_messages_by_user(item):
    try:
        # Check if the field exists and is greater than 0
        if isinstance(item, dict):
            item = [item]
        
        count=0
        for chat in item:
            if("chat_history" in chat and len(chat["chat_history"]) > 0):
                chat_history = chat["chat_history"]
                for message in chat_history:
                    if(message["role"] == "user"):
                        count += 1
        return count
    except Exception as e:
        print("Error in count_number_of_messages:", e)
        return 0

def count_searched_types(chat_object, flow_token):
    try:
        if isinstance(chat_object, dict):
            chat_object = [chat_object]
            
        types = []
        for chat in chat_object:
            chat_history = chat["chat_history"]
            for chat in chat_history:
                if chat["role"] == "user":
                    content = chat["content"]
                    if "Flow Reply" in content:
                        # print(content)
                        if flow_token in content:
                            matches = re.findall(r"screen_\d+_TextInput_\d+:\s*(.*)", content) or re.findall(r"screen_\d+_Professional_\d+:\s*(.*)", content)
                            types.extend([item.strip() for match in matches for item in match.split(",")])

        type_frequency = dict(Counter(types))
        
        return type_frequency

    except Exception as e:
        print("Error:", e)
        return {"error": str(e)}

def get_data(items):
    try:
        # count free notify trial
        free_notify_trial = count_free_notify_trial(items)
        
        # count free product discovery
        free_product_discovery = count_free_product_discovery(items)
        
        # count free custom done
        free_custom_done = count_free_custom_done(items)
        
        # count free professional discovery done
        free_professional_discovery_done = count_free_professional_discovery_done(items)
        
        # count free reservation done
        free_reservation_done = count_free_reservation_done(items)
        
        # count number of messages by user
        number_of_messages = count_number_of_messages_by_user(items)
        
        # count searched types
        product_searched_types = count_searched_types(items, "947206406740060")
        profession_searched_types = count_searched_types(items, "1099993468537230")
        
        # create a dictionary of all the analytics
        data = {
            "free_notify_trial": free_notify_trial,
            "free_product_discovery": free_product_discovery,
            "free_custom_done": free_custom_done,
            "free_professional_discovery_done": free_professional_discovery_done,
            "free_reservation_done": free_reservation_done,
            "number_of_messages": number_of_messages,
            "product_searched_types": product_searched_types,
            "profession_searched_types": profession_searched_types,
        }
        
        return json.loads(json.dumps(data))
    except Exception as e:
        print("Error:", e)
        return {"error": str(e)}
            

def analyse_user(user):
    try:
        if "user" not in user:
            user["user"] = "all"
        
        # Get all analytics of the user
        if user["user"] == "all":
            items = collection.find().to_list()
        else:
            items = collection.find({"whatsapp_username": {"$regex": f"^{user['user']}$", "$options": "i"}}).to_list()
        
        data = get_data(items)
        
        return data
        
    except Exception as e:
        print("Error:", e)
        return {"error": str(e)}
    
def get_chat_history(user):
    try:
        if "user" not in user:
            user["user"] = "all"
        # Get all anaytics of the user 
        if(user["user"] == "all"):    
            items = collection.find().to_list()
        else:
            items = collection.find({"whatsapp_username": {"$regex": f"^{user['user']}$", "$options": "i"}}).to_list()
        
        chat_history =[]
        for item in items:
            for chats in item["chat_history"]:
                chat_history.append(chats)
        
        return json.loads(json.dumps(chat_history))
    except Exception as e:
        print("Error:", e)
        return {"error": str(e)}
    
def list_users():
    try:
        items = collection.find().to_list()
        users = []
        for item in items:
            users.append(item["whatsapp_username"])
        return users
        
    except Exception as e:
        print("Error:", e)
        return {"error": str(e)}
    
def fetch_data_by_time_slot(from_time: str, to_time: str):
    try:
        # Convert 'DD-MM-YYTHH:MM:SS' to datetime objects
        from_date = datetime.strptime(from_time, "%d-%m-%yT%H:%M:%S")
        to_date = datetime.strptime(to_time, "%d-%m-%yT%H:%M:%S")

        # Query MongoDB for documents where 'created_at' is within the given time range
        items = collection.find({
            "created_at": {"$gte": from_date, "$lte": to_date}
        }).to_list(None)

        # If no data found
        if not items:
            return {"message": "No data found in the given time range"}

        # Extract and return relevant information
        data = get_data(items)
        return data

    except Exception as e:
        print("Error:", e)
        return {"error": str(e)}