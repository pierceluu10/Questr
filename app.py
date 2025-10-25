from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import time
from datetime import datetime, date
import random
import json
import os
from textblob import TextBlob

from models import db, User, Quest, UserQuest, Reflection, Achievement, UserAchievement

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///sidequestly.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Profile upload settings
app.config['PROFILE_UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'images', 'profiles')
ALLOWED_PROFILE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Create database tables
with app.app_context():
    # Ensure profile upload directory exists
    try:
        os.makedirs(app.config['PROFILE_UPLOAD_FOLDER'], exist_ok=True)
    except Exception as e:
        app.logger.error(f'Could not create profile upload folder: {e}')
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.context_processor
def inject_xp_globals():
    """Make total XP across all users and the current user's XP available in all templates."""
    try:
        total = db.session.query(db.func.coalesce(db.func.sum(User.xp), 0)).scalar()
    except Exception:
        total = 0

    user_xp = None
    if current_user and hasattr(current_user, 'is_authenticated') and current_user.is_authenticated:
        try:
            user_xp = int(current_user.xp or 0)
        except Exception:
            user_xp = 0

    return {
        'total_xp': int(total or 0),
        'user_xp': user_xp
    }

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
QUEST_TEMPLATES = {
    'Social': [
        {'title': 'Compliment someone today', 'description': 'Give a genuine compliment to a friend, family member, or colleague.', 'points': 15},
        {'title': 'Call someone you haven\'t talked to in a while', 'description': 'Reach out to an old friend or family member.', 'points': 20},
        {'title': 'Start a conversation with a stranger', 'description': 'Say hello to someone new in a coffee shop, elevator, or waiting area.', 'points': 25},
        {'title': 'Share something positive on social media', 'description': 'Post something uplifting or inspiring.', 'points': 10},
        {'title': 'Help someone with a small task', 'description': 'Offer assistance to someone who might need it.', 'points': 15}
    ],
    'Health': [
        {'title': 'Drink 8 glasses of water', 'description': 'Stay hydrated throughout the day.', 'points': 10},
        {'title': 'Take a 10-minute walk', 'description': 'Get some fresh air and light exercise.', 'points': 15},
        {'title': 'Do 20 push-ups or sit-ups', 'description': 'Get your heart pumping with some bodyweight exercises.', 'points': 20},
        {'title': 'Eat a healthy breakfast', 'description': 'Start your day with nutritious food.', 'points': 10},
        {'title': 'Stretch for 5 minutes', 'description': 'Take time to stretch your muscles and improve flexibility.', 'points': 10}
    ],
    'Mindfulness': [
        {'title': 'Meditate for 5 minutes', 'description': 'Take time to clear your mind and focus on your breathing.', 'points': 20},
        {'title': 'Write down 3 things you\'re grateful for', 'description': 'Practice gratitude by listing positive aspects of your life.', 'points': 15},
        {'title': 'Take 5 deep breaths', 'description': 'Practice mindful breathing to reduce stress.', 'points': 10},
        {'title': 'Spend 10 minutes in nature', 'description': 'Connect with the outdoors, even if just looking out a window.', 'points': 15},
        {'title': 'Practice positive self-talk', 'description': 'Say something kind to yourself in the mirror.', 'points': 15}
    ]
}

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
    categories = ['Social', 'Health', 'Mindfulness']
    today_quests = []
    
    for category in categories:
        template = random.choice(QUEST_TEMPLATES[category])
        
        # Check if quest already exists
        quest = Quest.query.filter_by(
            title=template['title'],
            category=category
        ).first()
        
        if not quest:
            quest = Quest(
                title=template['title'],
                category=category,
                description=template['description'],
                reward_points=template['points']
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


def allowed_profile_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_PROFILE_EXTENSIONS


@app.route('/profile/photo/upload', methods=['POST'])
@login_required
def upload_profile_photo():
    if 'photo' not in request.files:
        return jsonify({'success': False, 'error': 'No file part'}), 400

    file = request.files['photo']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No selected file'}), 400

    if file and allowed_profile_file(file.filename):
        filename = secure_filename(file.filename)
        ext = filename.rsplit('.', 1)[1].lower()
        # Build unique filename
        unique_name = f'user_{current_user.id}_{int(time.time())}.{ext}'
        save_path = os.path.join(app.config['PROFILE_UPLOAD_FOLDER'], unique_name)

        try:
            # Save new file
            file.save(save_path)

            # If user had previous uploaded file, try to remove it
            if current_user.profile_photo:
                try:
                    old_path = os.path.join(app.config['PROFILE_UPLOAD_FOLDER'], current_user.profile_photo)
                    if os.path.exists(old_path):
                        os.remove(old_path)
                except Exception:
                    app.logger.exception('Failed to remove old profile photo')

            # Update user record
            current_user.profile_photo = unique_name
            db.session.commit()

            photo_url = url_for('static', filename=f'images/profiles/{unique_name}')
            return jsonify({'success': True, 'url': photo_url}), 200
        except Exception as e:
            app.logger.error(f'Error saving profile photo: {e}')
            db.session.rollback()
            return jsonify({'success': False, 'error': 'Server error saving file'}), 500

    return jsonify({'success': False, 'error': 'Invalid file type'}), 400


@app.route('/profile/photo/reset', methods=['POST'])
@login_required
def reset_profile_photo():
    # Remove the file if exists and clear DB entry
    try:
        if current_user.profile_photo:
            file_path = os.path.join(app.config['PROFILE_UPLOAD_FOLDER'], current_user.profile_photo)
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except Exception:
                    app.logger.exception('Failed to remove profile photo during reset')

        current_user.profile_photo = None
        db.session.commit()

        default_url = url_for('static', filename='images/default-avatar.svg')
        return jsonify({'success': True, 'url': default_url}), 200
    except Exception as e:
        app.logger.error(f'Error resetting profile photo: {e}')
        db.session.rollback()
        return jsonify({'success': False, 'error': 'Server error'}), 500

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
