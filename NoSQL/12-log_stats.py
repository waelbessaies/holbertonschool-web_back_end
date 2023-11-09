#!/usr/bin/env python3
"""
Python function that changes all topics of a school document based on the name
"""
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient(
    'mongodb://your_username:your_password@your_host:your_port/')


db = client.logs
collection = db.nginx


total_logs = collection.count_documents({})


print(f"{total_logs} logs")


http_methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
print("Methods:")
for method in http_methods:
    count = collection.count_documents({"method": method})
    print(f"    method {method}: {count}")

special_log_count = collection.count_documents(
    {"method": "GET", "path": "/status"})
print(f"{special_log_count} status check")

client.close()
