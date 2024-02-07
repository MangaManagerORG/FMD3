# Use the official Python 3.10 image as the base image
FROM python:3.11

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir uvicorn


# Copy the rest of the application code to the working directory
COPY src/FMD3 FMD3
COPY src/FMD3_API FMD3_API
# Expose the port on which the app will run
EXPOSE 8000

# Specify the command to run the application
CMD [ "python", "-m", "FMD3_API" ]