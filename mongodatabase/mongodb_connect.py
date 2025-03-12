#!/usr/bin/env python3

import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Retrieve MongoDB URI from the environment variable
uri = os.getenv("MONGO_URI")

# Connect to MongoDB
client = MongoClient(uri)

# Access the liver_disease_db database
db = client.liver_disease_db
print("Connected to MongoDB!")
