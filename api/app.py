from flask import Flask
import os
import gridfs
from flask_socketio import SocketIO
import json
from bson import ObjectId
from user.database import db



class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super().default(obj)

# Initialize Flask app
app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = os.getenv('SECRET_KEY', '313a201b01ee3959c19396d09f3d21fb')

# app.json_encoder = CustomJSONEncoder 
# # Setting the path for uploaded files
# app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
# os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# # SocketIO initialization
# socketio = SocketIO(app)

# # MongoDB connection
# fs = gridfs.GridFS(db)

from user.routes import *

if __name__ == '__main__':
    app.run(debug=True)

