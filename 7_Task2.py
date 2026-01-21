from flask import Flask, render_template, request
from pymongo import MongoClient
import os
from dotenv import load_dotenv

app=Flask(__name__)
load_dotenv()
uri=os.getenv("mongodb_uri")

client=MongoClient(uri)

db=client["user_data"]
collection=db["new_users"]

@app.route("/",methods=["GET","POST"])
def user_data():
    if request.method=="POST":
        name=request.form["name"]
        email=request.form["email"]
        age=int(request.form["age"])

        collection.insert_one({
            "name":name,
            "email":email,
            "age":age
        })
        return "Done"
    client.close()
    return render_template("index.html")

if __name__=="__main__":
    app.run(debug=True)





