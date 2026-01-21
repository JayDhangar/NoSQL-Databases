import streamlit as st
from streamlit_autorefresh import st_autorefresh
from pymongo import MongoClient
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
import os
from flask import Flask ,request ,jsonify
from transformers import pipeline


load_dotenv()
app=Flask(__name__)

uri=os.getenv("mongodb_uri")
client=MongoClient(uri)

db=client["user_data"]
collection=db["data"]
genrator=pipeline("text-generation",model="gpt2")

@app.route("/generate",methods=["POST","GET"])
def user_data():
    data=request.json
    prompt=data.get("prompt")

    output=genrator(prompt,max_length=100)[0]["generated_text"]

    store_data={
        "Prompt":prompt,
        "output":output,
        "date_time":datetime.now()
    }
    collection.insert_one(store_data)
    if request.method=="GET":
        return "Work is done"
    
    return jsonify({
        "prompt":prompt,
        "output":output,
        "result":"data saved"
    })

st.set_page_config(page_title="Live MongoDB Results",layout="wide")
st.title("Live Data from MongoDB")
st.write("This app is connecte to MongoDB Atlas")
st_autorefresh(interval=5000, key="refresh")

data = list(db.data.find().sort({ "_id": -1 }).limit(1))

if data:
    df =pd.DataFrame(data)

    st.subheader("Result")
    st.dataframe(df,use_container_width=True)

    st.subheader("Generated Results")
    latest=data[0]

    st.write("Prompt",latest.get("Prompt"))
    st.write("Result",latest.get("output"))
    st.write("Timestamp",latest.get("date_time"))

else:
    st.warning("data not found")

if __name__=="__main__":
    app.run(debug=True)