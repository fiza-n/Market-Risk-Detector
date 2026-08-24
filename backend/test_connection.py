from db import client

try:
    client.admin.command('ping')
    print("Connected to MongoDB Atlas successfully!")
except Exception as e:
    print(e)