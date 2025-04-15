# Use Python 3.11 as the base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements.txt into the container
COPY requirements.txt /app/

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . /app/

# Copy the .env file into the container (if you're using .env for configurations)
COPY .env /app/

# Set environment variables for Flask
ENV FLASK_APP=app.__main__:app
ENV FLASK_RUN_HOST=0.0.0.0

# Expose the port Flask will run on
EXPOSE 5000

# Use flask run to start the Flask application
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
