# Base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the Python script to the container
COPY script.py .

# Install dependencies
RUN pip install selenium pymongo

# Download and install Chrome WebDriver
RUN apt-get update && apt-get install -y wget unzip && \
    wget -q https://chromedriver.storage.googleapis.com/94.0.4606.61/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip && \
    rm chromedriver_linux64.zip && \
    mv chromedriver /usr/local/bin/

# Set the entrypoint for the container
CMD [ "python", "script.py" ]
