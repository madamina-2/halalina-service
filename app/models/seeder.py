from app.models.job_type import JobType

def seed_job_types():
    job_types = [
        ('domestic worker', 'Pekerja Rumah Tangga'),
        ('construction worker', 'Pekerja Konstruksi'),
        ('factory worker', 'Pekerja Pabrik'),
        ('technician', 'Teknisi'),
        ('driver', 'Pengemudi'),
        ('security personnel', 'Personel Keamanan'),
        ('maintenance worker', 'Pekerja Pemeliharaan'),
        ('farmer', 'Petani'),
        ('manager', 'Manajer'),
        ('engineer', 'Insinyur'),
        ('accountant', 'Akuntan'),
        ('doctor', 'Dokter'),
        ('lawyer', 'Pengacara'),
        ('office staff', 'Staf Kantor'),
        ('analyst', 'Analis'),
        ('business owner', 'Pemilik Bisnis'),
        ('freelancer', 'Pekerja Lepas'),
        ('self-employed', 'Wiraswasta'),
        ('consultant', 'Konsultan'),
        ('retired', 'Pensiunan'),
        ('student', 'Mahasiswa')
    ]
    
    for label_en, label_id in job_types:
        value = label_en.replace(" ", "_").lower()  # Membuat nilai yang unik dari label_en
        try:
            # Cek apakah data sudah ada, jika belum insert
            if not JobType.query.filter_by(value=value).first():
                JobType.create(label_id, label_en, value)
                print(f'Added job type: {label_en}')
        except Exception as e:
            print(f"Failed to add job type {label_en}: {e}")

