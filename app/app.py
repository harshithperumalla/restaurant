from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Make this strong in production!

# File paths
USERS_FILE = 'users.json'
FEEDBACK_FILE = 'feedbacks.json'

# ------------------ Utility functions ------------------

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=4)

def load_feedbacks():
    if os.path.exists(FEEDBACK_FILE):
        with open(FEEDBACK_FILE, 'r') as f:
            return json.load(f)
    return []

def save_feedbacks(feedbacks):
    with open(FEEDBACK_FILE, 'w') as f:
        json.dump(feedbacks, f, indent=4)

# ------------------ Routes ------------------

@app.route('/')
def home():
    return render_template('index.html')  # Your landing page

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        mobile = request.form['mobile']
        password = request.form['password']
        recovery = request.form['recovery']

        users = load_users()

        if email in users:
            return 'User already exists. Please login.'

        users[email] = {
            'name': name,
            'mobile': mobile,
            'password': password,
            'recovery': recovery
        }
        save_users(users)
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        users = load_users()

        if email in users and users[email]['password'] == password:
            session['user'] = email
            return redirect(url_for('dashboard'))
        else:
            return 'Invalid credentials.'

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('Dash.html', user=session['user'])

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/menu')
def menu():
    # Example: serve static menu or connect to your API
    return render_template('menu.html')

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        names = request.form.getlist('name[]')
        restaurants = request.form.getlist('restaurant[]')
        feedbacks_text = request.form.getlist('feedback[]')

        feedbacks = load_feedbacks()

        for n, r, f in zip(names, restaurants, feedbacks_text):
            feedbacks.append({
                'name': n,
                'restaurant': r,
                'feedback': f
            })

        save_feedbacks(feedbacks)
        return 'Thank you! Your feedback has been submitted.'

    return render_template('feedback.html')

@app.route('/api/menu')
def api_menu():
    # Optional: send menu as JSON for a dynamic frontend
    menu_data = {
        "Ukusa": [
            {"item": "Ghee Roast Lamb Keema Bowl", "price": 690},
            {"item": "Aglio Olio Pasta", "price": 450},
            {"item": "Hazelnut Pancake", "price": 450}
        ],
        "Ram Ki Bandi": [
            {"item": "Schezwann Pizza Dosa", "price": 366},
            {"item": "Tawa Idly", "price": 177},
            {"item": "Cheese Upma", "price": 210}
        ]
        # Add more restaurants as needed
    }
    return jsonify(menu_data)

# ------------------ Run the app ------------------

if __name__ == '__main__':
    app.run(debug=True)
