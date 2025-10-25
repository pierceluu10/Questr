from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    xp = db.Column(db.Integer, default=0)
    streak = db.Column(db.Integer, default=0)
    join_date = db.Column(db.DateTime, default=datetime.utcnow)
    last_quest_date = db.Column(db.DateTime)
    
    # Relationships
    completed_quests = db.relationship('UserQuest', backref='user', lazy=True)
    reflections = db.relationship('Reflection', backref='user', lazy=True)
    achievements = db.relationship('UserAchievement', backref='user', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_level(self):
        return (self.xp // 100) + 1
    
    def get_xp_for_next_level(self):
        current_level = self.get_level()
        xp_needed = current_level * 100
        return xp_needed - self.xp
    
    def get_xp_progress_percentage(self):
        """Get XP progress as percentage for current level (0-100)"""
        return self.xp % 100

class Quest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # Social, Health, Mindfulness
    description = db.Column(db.Text)
    reward_points = db.Column(db.Integer, default=10)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    user_quests = db.relationship('UserQuest', backref='quest', lazy=True)

class UserQuest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quest_id = db.Column(db.Integer, db.ForeignKey('quest.id'), nullable=False)
    date_completed = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('user_id', 'quest_id', 'date_completed'),)

class Reflection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    sentiment_score = db.Column(db.Float)
    date = db.Column(db.DateTime, default=datetime.utcnow)

class Achievement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    icon = db.Column(db.String(50))  # emoji or icon class
    unlock_condition = db.Column(db.String(200))  # e.g., "streak_5", "xp_50"
    
    # Relationships
    user_achievements = db.relationship('UserAchievement', backref='achievement', lazy=True)

class UserAchievement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    achievement_id = db.Column(db.Integer, db.ForeignKey('achievement.id'), nullable=False)
    date_earned = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('user_id', 'achievement_id'),)
