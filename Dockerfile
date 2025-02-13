# Use the official Python image as the base
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Install necessary system dependencies
RUN apt-get update && apt-get install -y libpq-dev gcc python3-dev && rm -rf /var/lib/apt/lists/*

# Copy the initialization script
COPY entrypoint.sh /usr/local/bin/

# Make the script executable
RUN chmod +x /usr/local/bin/entrypoint.sh

# Expose the port on which Django will listen
EXPOSE 9000

# Set the initialization script as the entry point
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]