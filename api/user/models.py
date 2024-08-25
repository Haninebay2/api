from app import db
from passlib.hash import pbkdf2_sha256
from flask import session, jsonify, request
import uuid
import logging
from datetime import datetime
from werkzeug.utils import secure_filename
import os
from app import app

class User:
    @staticmethod
    def authenticate(username, password):
        user = db.users.find_one({"username": username})
        if user:
           if pbkdf2_sha256.verify(password, user['password']):
                print("Authentication successful")
                return user
           else:
                print("Password does not match")
        else:
            print("User not found")
        return None
    

    @staticmethod
    def signup(form_data):
        """Attempt to register a new user and return result as a dictionary."""
        user = {
            "_id": uuid.uuid4().hex,
            "username": form_data.get('username'),
            "email": form_data.get('email'),
            "password": pbkdf2_sha256.hash(form_data.get('password')),
            "role": form_data.get('role'),
            "profile_picture": "./images/user-1.png",  # Default profile picture
            "job_title": form_data.get('job_title', ''),
            "company": form_data.get('company', ''),
            "profile_views": 0,
            "post_views": 0,
            "connections": 0
        }
        if db.users.find_one({"email": user['email']}):
            return {"error": "Email address already in use"}, 400
        db.users.insert_one(user)
        del user['password']  # Remove password for security reasons
        return user, 200

    
    
