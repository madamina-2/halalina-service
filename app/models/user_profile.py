from . import db
from .job_type import JobType  # Impor JobType model

class UserProfile(db.Model):
    __tablename__ = 'user_profile'

    # Kolom untuk UserProfile
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    job_type_id = db.Column(db.Integer, db.ForeignKey('job_type.id'), nullable=False)  # ForeignKey ke JobType
    job_type = db.relationship('JobType', backref='user_profiles')  # Relasi dengan JobType
    
    # Menggunakan String untuk status pernikahan dan kategori usia
    married = db.Column(db.String(20))  # String untuk status pernikahan ('single', 'married')
    debt_type = db.Column(db.ARRAY(db.String))  # Array untuk menyimpan tipe hutang
    account_balance = db.Column(db.Integer)
    age_group = db.Column(db.String(20))  # String untuk kategori usia ('gen_Z', 'millennials', 'gen_X')

    def __repr__(self):
        return f'<UserProfile {self.id} for User {self.user_id}>'

    # Method untuk membuat profile baru
    @classmethod
    def create(cls, user_id, job_type_id, married, debt_type, account_balance, age_group):
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

    # Mendapatkan profile berdasarkan user_id
    @classmethod
    def get_profile_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).first()

    # Mendapatkan semua profile
    @classmethod
    def get_all_profiles(cls):
        return cls.query.all()
