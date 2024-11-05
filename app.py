from flask import Flask, render_template, request, redirect, url_for, flash, session ,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import json
from price_tracker import fetch_data
import os

# Load environment variables from variables.env file
dotenv_path = 'F:/pricetracker_project/variables.env'
load_dotenv(dotenv_path=dotenv_path)

admin_username = os.getenv('ADMIN_USERNAME')
admin_password = os.getenv('ADMIN_PASSWORD')

# Load config.json
with open('config.json') as config_file:
    config = json.load(config_file)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///F:/pricetracker_project/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
os.environ['SQLALCHEMY_SILENCE_UBER_WARNING'] = '1'


db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'user_login'  # Default login view for Flask-Login

# User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_tables():
    with app.app_context():
        db.create_all()

# Call create_tables when app starts
create_tables()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user_login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            if user.is_admin:
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('user_dashboard'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('user_login.html')

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == admin_username and password == admin_password:
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Admin Login Unsuccessful. Please check username and password', 'danger')
    return render_template('admin_login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already exists. Please use a different email.', 'danger')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created! You can now login.', 'success')
        return redirect(url_for('user_login'))
    return render_template('register.html')

@app.route('/user_dashboard')
@login_required
def user_dashboard():
    return render_template('user_dashboard.html')

@app.route('/admin_dashboard')
@login_required
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    return render_template('admin_dashboard.html', config=config)


@app.route('/track', methods=['POST'])
def track():
    product_link = request.form.get('product_link')
    threshold_value = request.form.get('threshold_value')
    recipient_email = request.form.get('recipient_email')

    if not product_link or not threshold_value or not recipient_email:
        return jsonify({"status": "error", "message": "Product link, threshold value, and recipient email are required"}), 400

    try:
        fetch_data(product_link, float(threshold_value), recipient_email)
        return jsonify({"status": "success", "message": "Tracking started successfully!"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error occurred: {e}"}), 500



@app.route('/update_selectors', methods=['GET', 'POST'])
@login_required
def update_selectors():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    if request.method == 'POST':
        title_selector = request.form['title_selector']
        price_selector = request.form['price_selector']
        config['title_selector'] = title_selector
        config['price_selector'] = price_selector
        with open('config.json', 'w') as config_file:
            json.dump(config, config_file)
        flash('Selectors updated successfully.', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('update_selectors.html', config=config)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('admin_logged_in', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
