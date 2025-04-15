# Gunakan image Python 3.11 sebagai base image
FROM python:3.11-slim

# Set working directory di dalam container
WORKDIR /app

# Menyalin file requirements.txt ke dalam container
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Menyalin seluruh project ke dalam container
COPY . /app/

# Menyalin .env ke dalam container (Jika Anda menggunakan file .env untuk konfigurasi)
COPY .env /app/

# Set environment variable agar Flask berjalan di mode produksi
ENV FLASK_APP=__main__.py
ENV FLASK_RUN_HOST=0.0.0.0

# Set FLASK_ENV untuk menentukan mode (development, production, atau local)
# Ganti dengan 'development' atau 'local' sesuai kebutuhan
ENV FLASK_ENV=development  

# Gunakan Gunicorn untuk menjalankan Flask dalam mode produksi
# Install Gunicorn untuk produksi

RUN pip install gunicorn  
# Port yang akan digunakan oleh Flask
EXPOSE 5000

# Gunakan Gunicorn untuk menjalankan aplikasi Flask di produksi
CMD ["gunicorn", "-b", "0.0.0.0:5000", "__main__:app"]
