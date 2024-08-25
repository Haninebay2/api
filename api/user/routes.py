from datetime import datetime
from functools import wraps
from flask import request, session, redirect, url_for, render_template, jsonify, flash
from app import app
from user.models import User
import os
from bson import ObjectId
import requests
from app import API_KEY
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session or session.get('username') != 'admin':
            flash('Access denied. Admins only.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def home():
    # user = session.get('user')

    # # Fetch user details for each post without converting to ObjectId
    # for post in posts:
    #     user_details = db.users.find_one({"_id": post['user_id']})  # Assuming user_id is stored as a string
    #     if user_details:
    #         post['user'] = {
    #             'username': user_details.get('username', 'Unknown User'),
    #             'profile_picture': user_details.get('profile_picture', 'default.jpg')
    #         }

    # print(f"User in session: {user}")  # Debugging line
    return render_template('index.html')



def start_session(user):
    """Initialize user session after successful login."""
    del user['password']  # Remove password before storing user in session
    session['logged_in'] = True
    session['user'] = user
    print(f"User stored in session: {user}")  # Debugging line
    return jsonify({"redirect": url_for('home')}), 200

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.authenticate(username, password)
        if user:
            user_data = {k: str(v) if isinstance(v, ObjectId) else v for k, v in user.items()}
            print(f"User data after authentication: {user_data}")  # Debugging line
            return start_session(user_data)
        else:
            return jsonify({"error": "Invalid credentials"}), 401
    return render_template('login.html')

@app.route('/user/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user_data, status = User.signup(request.form)
        if status == 200:
            print(f"User before storing in session: {user_data}")  # Debugging line
            session['user'] = user_data
            session['logged_in'] = True

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'success': 'Signup successful'}), 200
            else:
                return redirect(url_for('home'))

        else:
            error_message = user_data.get('error', 'Signup failed. Please try again.')
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'error': error_message}), 400
            else:
                return render_template('SignUp.html', error=error_message)
    return render_template('SignUp.html')

@app.route('/signout')
@login_required
def signout():
    session.pop('logged_in', None)
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/HowItWorks')
def HowItWorks():
    # user = session.get('user')

    # # Fetch user details for each post without converting to ObjectId
    # for post in posts:
    #     user_details = db.users.find_one({"_id": post['user_id']})  # Assuming user_id is stored as a string
    #     if user_details:
    #         post['user'] = {
    #             'username': user_details.get('username', 'Unknown User'),
    #             'profile_picture': user_details.get('profile_picture', 'default.jpg')
    #         }

    # print(f"User in session: {user}")  # Debugging line
    return render_template('HowItWorks.html')
    
@app.route('/Search')
def Search():
    # user = session.get('user')

    # # Fetch user details for each post without converting to ObjectId
    # for post in posts:
    #     user_details = db.users.find_one({"_id": post['user_id']})  # Assuming user_id is stored as a string
    #     if user_details:
    #         post['user'] = {
    #             'username': user_details.get('username', 'Unknown User'),
    #             'profile_picture': user_details.get('profile_picture', 'default.jpg')
    #         }

    # print(f"User in session: {user}")  # Debugging line
    return render_template('Search.html')


@app.route('/search', methods=['POST'])
def search_api():
    query = request.json.get('query')
    if not query:
        return jsonify({'error': 'No query provided'}), 400

    # Step A: Generate a Roadmap using OpenAI
    roadmap = generate_roadmap(query)
    
    # Step B: Generate content based on the roadmap
    content = generate_content_based_on_roadmap(roadmap)
    
    return jsonify(content)

def generate_roadmap(query):
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }
    data = {
        "prompt": f"Generate a learning roadmap based on the following topic: {query}",
        "max_tokens": 150
    }
    response = requests.post("https://api.openai.com/v1/engines/text-davinci-002/completions", json=data, headers=headers)
    roadmap = response.json().get('choices')[0].get('text', '')
    return roadmap

def generate_content_based_on_roadmap(roadmap):
    # Simulate content generation based on roadmap
    # This is where you could have logic to parse the roadmap and generate specific courses or problems
    # For demonstration, this just returns a static response
    return {
        "roadmap": roadmap,
        "courses": ["Course 1", "Course 2", "Course 3"],
        "problems": ["Problem 1", "Problem 2"]
    }

if __name__ == '__main__':
    app.run(debug=True)
