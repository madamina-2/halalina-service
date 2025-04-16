from . import db
from sqlalchemy.exc import IntegrityError

class UserProfile(db.Model):
    __tablename__ = 'user_profile'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    job_type_id = db.Column(db.Integer, db.ForeignKey('job_type.id'), nullable=False)
    job_type = db.relationship('JobType', backref='user_profiles')
    married = db.Column(db.String(20))
    debt_type = db.Column(db.ARRAY(db.String))
    account_balance = db.Column(db.Integer)
    age_group = db.Column(db.String(20))

    def __repr__(self):
        return f'<UserProfile {self.id} for User {self.user_id}>'

    @classmethod
    def create(cls, user_id, job_type_id, married, debt_type, account_balance, age_group):
        try:
            existing_profile = cls.query.filter_by(user_id=user_id).first()
            if existing_profile:
                raise ValueError(f"Profile with user_id {user_id} already exists.")

            new_profile = cls(
                user_id=user_id,
                job_type_id=job_type_id,
                married=married,
                debt_type=debt_type,
                account_balance=account_balance,
                age_group=age_group
            )
            db.session.add(new_profile)
            db.session.commit()
            return new_profile
        except IntegrityError as e:
            db.session.rollback()
            raise ValueError("Integrity error occurred, possibly due to unique constraint violation: " + str(e))
        except Exception as e:
            db.session.rollback()
            raise ValueError("Failed to create profile: " + str(e))

    @classmethod
    def get_profile_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).first()

    @classmethod
    def get_all_profiles(cls):
        return cls.query.all()

    @staticmethod
    def validate_age_group(age_group):
        valid_age_groups = ['gen_Z', 'millennials', 'gen_X']
        if age_group not in valid_age_groups:
            raise ValueError("Age group harus salah satu dari: 'gen_Z', 'millennials', 'gen_X'.")

    @staticmethod
    def validate_marital_status(married):
        valid_status = ['single', 'married']
        if married not in valid_status:
            raise ValueError("Married status harus salah satu dari: 'single', 'married'.")
