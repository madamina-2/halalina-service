from . import db

class JobType(db.Model):
    __tablename__ = 'job_type'  # Nama tabel di database

    # Kolom-kolom tabel job_type
    id = db.Column(db.Integer, primary_key=True)  # Primary key
    label_id = db.Column(db.String(255), nullable=False)  # Label dalam bahasa Indonesia
    label_en = db.Column(db.String(255), nullable=False)  # Label dalam bahasa Inggris
    value = db.Column(db.String(100), unique=True, nullable=False)  # Nilai unik untuk job type

    def __repr__(self):
        return f'<JobType {self.label_en}>'

    @classmethod
    def create(cls, label_id, label_en, value):
        """Fungsi untuk membuat job type baru"""
        new_job_type = cls(label_id=label_id, label_en=label_en, value=value)
        db.session.add(new_job_type)
        db.session.commit()
        return new_job_type

    @classmethod
    def get_all_job_types(cls):
        """Fungsi untuk mendapatkan semua job types"""
        return cls.query.all()

    @classmethod
    def get_job_type_by_value(cls, value):
        """Fungsi untuk mendapatkan job type berdasarkan value"""
        return cls.query.filter_by(value=value).first()
