# Use the official Python image from Docker Hub
FROM python:3.11

# Set the working directory inside the container
WORKDIR /app

# Copy the poetry.lock and pyproject.toml files to the container
COPY pyproject.toml poetry.lock /app/

# Install poetry
RUN pip install poetry

# Install dependencies
RUN poetry install --no-root

# Copy the application code to the container
COPY . /app

# Expose the port on which the Flask app will run
EXPOSE 5000

# Command to run the Flask app using Gunicorn
CMD ["poetry", "run", "gunicorn", "-b", "0.0.0.0:5000", "src.buildpy3.app:app"]