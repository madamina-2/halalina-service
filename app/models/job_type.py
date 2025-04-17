from . import db

class JobType(db.Model):
    __tablename__ = 'job_type'

    id = db.Column(db.Integer, primary_key=True)
    label_id = db.Column(db.String(255), nullable=False)
    label_en = db.Column(db.String(255), nullable=False)
    value = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f'<JobType {self.label_en}>'

    @classmethod
    def create(cls, label_id, label_en, value):
        try:
            new_job_type = cls(label_id=label_id, label_en=label_en, value=value)
            db.session.add(new_job_type)
            db.session.commit()
            return new_job_type
        except Exception as e:
            db.session.rollback()
            raise ValueError("Gagal membuat job type: " + str(e))

    @classmethod
    def get_all_job_types(cls):
        return cls.query.all()

    @classmethod
    def get_job_type_by_value(cls, value):
        return cls.query.filter_by(value=value).first()
