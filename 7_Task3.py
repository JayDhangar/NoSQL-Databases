from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime
from transformers import pipeline
import os
from dotenv import load_dotenv

app=Flask(__name__)

load_dotenv()
uri=os.getenv("mongodb_uri")

genrator=pipeline("text-generation",model="gpt2")
client=MongoClient(uri)
db=client["user_data"]
collection=db["data"]

@app.route("/generate",methods=["POST","GET"])
def user_data():
    data=request.json
    prompt=data.get("prompt")

    output=genrator(prompt,max_length=50)[0]["generated_text"]

    store_data={
        "Prompt":prompt,
        "output":output,
        "date_time":datetime.now()
    }
    collection.insert_one(store_data)
    if request.method=="GET":
        return "Work is done"
    client.close()
    return jsonify({
        "prompt":prompt,
        "output":output,
        "result":"data saved"
    })

if __name__=="__main__":
    app.run(debug=True)