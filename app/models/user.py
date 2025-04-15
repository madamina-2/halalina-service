from . import db
from models.user_profile import UserProfile  # Pastikan untuk mengimpor UserProfile

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(20), nullable=True)

    # Relasi One-to-One dengan UserProfile
    user_profile = db.relationship('UserProfile', backref='user', uselist=False)

    def __repr__(self):
        return f'<User {self.full_name}>'

    @classmethod
    def create(cls, full_name, email, password_hash, phone_number=None):
        new_user = cls(full_name=full_name, email=email, password_hash=password_hash, phone_number=phone_number)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @classmethod
    def get_user_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def get_all_users(cls):
        return cls.query.all()

    @classmethod
    def get_user_by_phone_number(cls, phone_number):
        return cls.query.filter_by(phone_number=phone_number).first()
