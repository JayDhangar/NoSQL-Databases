# import firebase_admin
# from firebase_admin import db , credentials
# from dotenv import load_dotenv
# from openai import OpenAI
# from datetime import datetime

# load_dotenv()
# # openai.API=os.getenv("api_key")

# cred= credentials.Certificate("firebasek.json")
# firebase_admin.initialize_app(cred,{"databaseURL":"https://my-project-e5d79-default-rtdb.asia-southeast1.firebasedatabase.app/"})
# client=OpenAI()
# ref =db.reference("/")

# def bot_response(user_message):
#     responce=client.chat.completions.create(model="gpt-3.5-turbo",messages=[{"role":"system","content":"Hello"},{"role":"user","content":user_message}])

#     return responce ["choices"][0]["message"]["content"]

# def store_chat(user_id,user_msg,bot_msg):
#     chat_ref=ref.child("chats").child(user_id).push()
#     chat_ref.set({
#         "user_message":user_msg,
#         "bot_message":bot_msg,
#         "time_stamp":datetime.utcnow().isoformat()
#     })

# if __name__=="__main__":
#     user_id="user_001"

#     while True:
#         user_input=input("User:")

#         if user_input.lower() in ["exit", "quit"]:
#             print("Chat ended.")
#             break

#         bot_reply = bot_response(user_input)
#         print("Bot:", bot_reply)

#         store_chat(user_id, user_input, bot_reply)


import firebase_admin
from firebase_admin import db, credentials
from transformers import pipeline
from datetime import datetime

chatbot = pipeline(
    "text-generation",
    model="distilgpt2"  
)

cred = credentials.Certificate("firebasek.json")
firebase_admin.initialize_app(
    cred,{"databaseURL": "https://my-project-e5d79-default-rtdb.asia-southeast1.firebasedatabase.app/"}
)

ref = db.reference("/")

def bot_response(user_message):
    result = chatbot(
        user_message,
        max_length=100,
        do_sample=True,
        temperature=0.7,
        truncation=True
    )
    return result[0]["generated_text"]

def store_chat(user_id, user_msg, bot_msg):
    ref.child("chats").child(user_id).push({
        "user_message": user_msg,
        "bot_message": bot_msg,
        "timestamp": datetime.utcnow().isoformat()
    })

if __name__ == "__main__":
    user_id = "user_001"
    print("Local AI Chatbot started (type 'exit' to quit)\n")

    while True:
        user_input = input("User: ")

        if user_input.lower() in ["exit", "quit"]:
            print("Chat ended.")
            break

        bot_reply = bot_response(user_input)
        print("Bot:", bot_reply)

        store_chat(user_id, user_input, bot_reply)

