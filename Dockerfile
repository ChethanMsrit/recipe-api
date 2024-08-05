# Use the official Python image from the Docker Hub
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . /app/

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
# CMD ["python", "manage.py", "runserver"]

CMD ["sh", "-c", "python manage.py makemigrations && python manage.py migrate && python manage.py runserver"]
