from db.collections import waitlist_collection

def get_waiting_persons():
    try:
        data = waitlist_collection.find().to_list(None)
        names = {}
        for person in data:
            if person["name"] and str(person["name"]) != "nan":
                names[str(person["name"])] =(str(person["phone_number"]), str(person["use_case"]))
        return {"Total Waiting": len(names), "Persons": names}
    except Exception as e:
        print("Error in get_waiting_persons:", e)
        return []
    