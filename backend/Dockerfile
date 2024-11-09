# Use an official Python image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the rest of the app’s code and .env file
COPY . .

# Run your main application
CMD ["python", "main.py"]
