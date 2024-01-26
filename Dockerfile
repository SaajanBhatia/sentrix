# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install Gunicorn and any other needed packages specified in requirements.txt
RUN pip install gunicorn && pip install --no-cache-dir -r requirements.txt

# Make port 4030 available to the world outside this container
EXPOSE 4030

# Define environment variable
ENV NAME Sentrix
ENV FLASK_ENV=production

# Run app with Gunicorn when the container launches
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:4030", "run:app"]
