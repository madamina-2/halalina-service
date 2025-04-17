# Gunakan image Python 3.11 sebagai base image
FROM python:3.11-slim

# Install curl
RUN apt-get update && apt-get install -y curl

# Set working directory di dalam container
WORKDIR /app

# Menyalin file requirements.txt ke dalam container
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Menyalin seluruh project ke dalam container
COPY . /app/

# Set environment variable agar Flask berjalan di mode produksi
ENV FLASK_APP=app.__main__:app
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5002
# Install Gunicorn
RUN pip install gunicorn  

# Port yang akan digunakan oleh Flask
EXPOSE 5002

# Gunakan Gunicorn untuk menjalankan aplikasi Flask
CMD ["gunicorn", "-b", "0.0.0.0:5002", "app.__main__:app"]
