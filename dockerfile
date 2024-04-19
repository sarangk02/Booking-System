FROM python:3.10-slim-bullseye

# Set the working directory
WORKDIR /booking_system

# Copy the current directory contents into the container at /booking_system
COPY . /booking_system

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt && python -m pip install --upgrade pip