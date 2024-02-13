# Use an official Python runtime as a parent image
FROM python:3.9

# Set environment variables for your application
ENV APP_HOME /app
ENV PYTHONUNBUFFERED 1

# Create and set the working directory
WORKDIR $APP_HOME

# Install curl
RUN apt-get update && apt-get install -y curl

# Copy the pyproject.toml and poetry.lock files into the container
COPY pyproject.toml poetry.lock ./

# Install Poetry
RUN pip install poetry


##WIP