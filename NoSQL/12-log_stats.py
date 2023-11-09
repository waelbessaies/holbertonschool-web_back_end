#!/usr/bin/env python3
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient(
    'mongodb://your_username:your_password@your_host:your_port/')

# Choose the database and collection
db = client.logs
collection = db.nginx

# Get the total number of logs
total_logs = collection.count_documents({})

# Display the total number of logs
print(f"{total_logs} logs")

# Display the number of logs for each HTTP method
http_methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
print("Methods:")
for method in http_methods:
    count = collection.count_documents({"method": method})
    print(f"    method {method}: {count}")

# Display the number of logs with method=GET and path=/status
special_log_count = collection.count_documents(
    {"method": "GET", "path": "/status"})
print(f"{special_log_count} status check")

# Close the MongoDB connection
client.close()
