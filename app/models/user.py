from . import db
from sqlalchemy import func

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(20), nullable=True)
    terms_conditions = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=func.now())  # Adding created_at field

    # Relasi One-to-One dengan UserProfile
    user_profile = db.relationship('UserProfile', backref='user', uselist=False)

    def __repr__(self):
        return f'<User {self.full_name}>'

    @classmethod
    def create(cls, full_name, email, password_hash, phone_number=None, terms_conditions=True):
        try:
            new_user = cls(full_name=full_name, email=email, password_hash=password_hash, phone_number=phone_number, terms_conditions=terms_conditions)
            db.session.add(new_user)
            db.session.commit()
            return new_user
        except Exception as e:
            db.session.rollback()  # Rollback jika ada error
            raise ValueError("Gagal membuat user: " + str(e))

    @classmethod
    def get_user_by_email(cls, email):
        return cls.query.filter_by(email=email).first()
    
    @classmethod
    def get_user_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def get_all_users(cls):
        return cls.query.all()

    @classmethod
    def get_user_by_phone_number(cls, phone_number):
        return cls.query.filter_by(phone_number=phone_number).first()
