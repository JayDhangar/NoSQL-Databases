from flask import Flask, jsonify
from pymongo import MongoClient
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()
app=Flask(__name__)

uri=os.getenv("mongodb_uri")
client=MongoClient(uri)

db = client["user_data"]         
collection = db["data"]

@app.route("/today",methods=["GET"])
def data():
    todays_data=datetime.utcnow().replace(hour=0,minute=0,second=0,microsecond=0)
    tomorrow=todays_data+timedelta(days=1)

    find=collection.find({
        "date_time":{"$gte":todays_data,"$lt":tomorrow}
    })
    
    result=[]
    for doc in find:
        result.append({
            "Prompt":doc.get("Prompt"),
            "output":doc.get("output"),
            "date_time":doc.get("date_time")

        })
        return jsonify(result)
    client.close()
if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
