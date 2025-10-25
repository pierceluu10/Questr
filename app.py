from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date
import random
import json
import os
from textblob import TextBlob

from models import db, User, Quest, UserQuest, Reflection, Achievement, UserAchievement

#Code for Gemini API:
#First, we need to setup for Gemini API
#MAKE SURE TO ADD THE USER DESCRIPTION PART
User_description = "Hello, I am a first year Computer Engineering Student"
GEMINI_API_KEY = "AIzaSyDVaYgw1kOSJ6p8AyTP6rRlH1jEfdkmdvM"

import json
from google import genai
from google.genai import types
client = genai.Client(api_key=GEMINI_API_KEY)

#Define Structure for ouput of prompt
quest_schema=types.Schema(
    type=types.Type.OBJECT,
    properties={
            "social_title":types.Schema(type=types.Type.STRING, description="Title of the social sidequest"),
            "social_description":types.Schema(type=types.Type.STRING, description="Description of the social sidequest"),
            "social_points":types.Schema(type=types.Type.INTEGER, description="Point value of the social sidequest"),
            "health_title":types.Schema(type=types.Type.STRING, description="Title of the health sidequest"),
            "health_description":types.Schema(type=types.Type.STRING, description="Description of the health sidequest"),
            "health_points":types.Schema(type=types.Type.INTEGER, description="Point value of the health sidequest"),
            "mindfulness_title":types.Schema(type=types.Type.STRING, description="Title of the mindfulness sidequest"),
            "mindfulness_description":types.Schema(type=types.Type.STRING, description="Description of the mindfulness sidequest"),
            "mindfulness_points":types.Schema(type=types.Type.INTEGER, description="Point value of the mindfulness sidequest"),
    },
    required=[
        "social_title", "social_description", "social_points",
        "health_title", "health_description", "health_points",
        "mindfulness_title", "mindfulness_description", "mindfulness_points"
    ]
)
prompt = f'"Using the description of the user: {User_description}, taking into account their interests and personal wellbeing needs, generate 3 side quests for the user throughout the day. There should be one sidequest for Social, one for Health, and one for Mindfulness. Each sidequest should have a title, a brief description, and a reward point value between 10 and 30 points. Make sure the sidequests are not corny or generic. Each quest should 80 characters or less. Make sure the points are appropriate for the difficulty and impact of the sidequest. Make sure the sidequests are diverse and engaging, that the person doing them has a guranteed chance of being able to complete them (i.e. do not assume they have a coding class, ask them to work on code in general)."'





app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///sidequestly.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Create database tables
with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Forms
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Register')

class ReflectionForm(FlaskForm):
    text = TextAreaField('How did this make you feel?', validators=[DataRequired()])
    submit = SubmitField('Submit Reflection')



# Quest data
def get_daily_quests(user_id):
    """Get or generate today's quests for a user"""
    today = date.today()
    
    # Check if user already has quests for today
    existing_quests = Quest.query.filter(
        Quest.id.in_(
            db.session.query(UserQuest.quest_id).filter(
                UserQuest.user_id == user_id,
                db.func.date(UserQuest.date_completed) == today
            )
        )
    ).all()
    
    if existing_quests:
        return existing_quests
    
    # Generate new quests for today
    today_quests = []
    response = client.models.generate_content(
        model="gemini-2.5-flash", 
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=quest_schema
        )
    )
    categories = ['Social', 'Health', 'Mindfulness']
    
    try:
        quests_data=json.loads(response.text)
    
        social_title = quests_data["social_title"]
        social_description = quests_data["social_description"]
        social_points = quests_data["social_points"]
        health_title = quests_data["health_title"]
        health_description = quests_data["health_description"]
        health_points = quests_data["health_points"]
        mindfulness_title = quests_data["mindfulness_title"]
        mindfulness_description = quests_data["mindfulness_description"]
        mindfulness_points = quests_data["mindfulness_points"]    
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON output: {e}")
        print("Raw response text:", response.text)
        
    social_quest = quest(
        title = social_title,
        category = 'Social',
        description = social_description,
        reward_points = social_points
    )
    db.session.add(quest)
    db.session.commit()
    today_quests.append(quest)

    
    health_quest = quest(
        title = health_title,
        category = 'Health',
        description = health_description,
        reward_points = health_points
    )
    db.session.add(quest)
    db.session.commit()
    today_quests.append(quest)

    mindfulness_quest = quest(
        title = mindfulness_title,
        category = 'Mindfulness',
        description = mindfulness_description,
        reward_points = mindfulness_points
    )
    db.session.add(quest)
    db.session.commit()
    today_quests.append(quest)
    return today_quests

def check_achievements(user):
    """Check and award achievements for a user"""
    achievements_to_check = [
        {'condition': 'streak_5', 'title': 'Motivation Master', 'description': 'Maintain a 5-day streak!', 'icon': '🔥'},
        {'condition': 'streak_10', 'title': 'Streak Champion', 'description': 'Maintain a 10-day streak!', 'icon': '⚡'},
        {'condition': 'xp_50', 'title': 'Level 2 Explorer', 'description': 'Earn 50 XP!', 'icon': '⭐'},
        {'condition': 'xp_100', 'title': 'Quest Veteran', 'description': 'Earn 100 XP!', 'icon': '🏆'},
        {'condition': 'quests_10', 'title': 'SideQuest Veteran', 'description': 'Complete 10 quests!', 'icon': '🎯'},
        {'condition': 'quests_25', 'title': 'Quest Master', 'description': 'Complete 25 quests!', 'icon': '👑'}
    ]
    
    for achievement_data in achievements_to_check:
        condition = achievement_data['condition']
        achievement = Achievement.query.filter_by(unlock_condition=condition).first()
        
        if not achievement:
            achievement = Achievement(
                title=achievement_data['title'],
                description=achievement_data['description'],
                icon=achievement_data['icon'],
                unlock_condition=condition
            )
            db.session.add(achievement)
            db.session.commit()
        
        # Check if user already has this achievement
        user_achievement = UserAchievement.query.filter_by(
            user_id=user.id,
            achievement_id=achievement.id
        ).first()
        
        if not user_achievement:
            should_award = False
            
            if condition == 'streak_5' and user.streak >= 5:
                should_award = True
            elif condition == 'streak_10' and user.streak >= 10:
                should_award = True
            elif condition == 'xp_50' and user.xp >= 50:
                should_award = True
            elif condition == 'xp_100' and user.xp >= 100:
                should_award = True
            elif condition == 'quests_10' and len(user.completed_quests) >= 10:
                should_award = True
            elif condition == 'quests_25' and len(user.completed_quests) >= 25:
                should_award = True
            
            if should_award:
                user_achievement = UserAchievement(
                    user_id=user.id,
                    achievement_id=achievement.id
                )
                db.session.add(user_achievement)
                db.session.commit()

# Routes
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid username or password')
    
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        try:
            if User.query.filter_by(username=form.username.data).first():
                flash('Username already exists')
                return render_template('register.html', form=form)
            
            if User.query.filter_by(email=form.email.data).first():
                flash('Email already registered')
                return render_template('register.html', form=form)
            
            user = User(
                username=form.username.data,
                email=form.email.data
            )
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            
            login_user(user)
            return redirect(url_for('dashboard'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred during registration. Please try again.')
            app.logger.error(f'Registration error: {str(e)}')
            return render_template('register.html', form=form)
    
    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    quests = get_daily_quests(current_user.id)
    check_achievements(current_user)
    
    # Get user's completed quests for today
    today = date.today()
    completed_today = UserQuest.query.filter(
        UserQuest.user_id == current_user.id,
        db.func.date(UserQuest.date_completed) == today
    ).all()
    
    completed_quest_ids = [uq.quest_id for uq in completed_today]
    
    return render_template('dashboard.html', 
                         quests=quests, 
                         completed_quest_ids=completed_quest_ids,
                         user=current_user)

@app.route('/complete/<int:quest_id>')
@login_required
def complete_quest(quest_id):
    quest = Quest.query.get_or_404(quest_id)
    today = date.today()
    
    # Check if already completed today
    existing = UserQuest.query.filter(
        UserQuest.user_id == current_user.id,
        UserQuest.quest_id == quest_id,
        db.func.date(UserQuest.date_completed) == today
    ).first()
    
    if existing:
        flash('Quest already completed today!')
        return redirect(url_for('dashboard'))
    
    # Mark quest as completed
    user_quest = UserQuest(
        user_id=current_user.id,
        quest_id=quest_id
    )
    db.session.add(user_quest)
    
    # Update user XP and streak
    current_user.xp += quest.reward_points
    
    # Update streak logic
    if current_user.last_quest_date != today:
        if current_user.last_quest_date and (today - current_user.last_quest_date.date()).days == 1:
            current_user.streak += 1
        else:
            current_user.streak = 1
        current_user.last_quest_date = datetime.utcnow()
    
    db.session.commit()
    
    flash(f'Quest completed! +{quest.reward_points} XP')
    return redirect(url_for('dashboard'))

@app.route('/reflection/<int:quest_id>', methods=['GET', 'POST'])
@login_required
def reflection(quest_id):
    quest = Quest.query.get_or_404(quest_id)
    form = ReflectionForm()
    
    if form.validate_on_submit():
        # Calculate sentiment score
        blob = TextBlob(form.text.data)
        sentiment_score = blob.sentiment.polarity
        
        reflection = Reflection(
            user_id=current_user.id,
            text=form.text.data,
            sentiment_score=sentiment_score
        )
        db.session.add(reflection)
        db.session.commit()
        
        flash('Reflection saved!')
        return redirect(url_for('dashboard'))
    
    return render_template('reflection.html', form=form, quest=quest)

@app.route('/profile')
@login_required
def profile():
    # Get user's reflection data for mood chart
    reflections = Reflection.query.filter_by(user_id=current_user.id).order_by(Reflection.date.desc()).limit(30).all()
    
    # Get user's achievements
    user_achievements = UserAchievement.query.filter_by(user_id=current_user.id).all()
    
    return render_template('profile.html', 
                         user=current_user, 
                         reflections=reflections,
                         achievements=user_achievements)

@app.route('/api/mood-data')
@login_required
def mood_data():
    reflections = Reflection.query.filter_by(user_id=current_user.id).order_by(Reflection.date).all()
    
    data = {
        'dates': [r.date.strftime('%Y-%m-%d') for r in reflections],
        'scores': [r.sentiment_score for r in reflections]
    }
    
    return jsonify(data)

if __name__ == '__main__':
    # Only run in debug mode if not in production
    import os
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    app.run(debug=debug_mode, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
