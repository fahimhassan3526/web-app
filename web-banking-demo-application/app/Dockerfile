
FROM python:3.9

# Set the working directory to /app
WORKDIR /wow

# Copy the current directory contents into the container at /app
COPY . /wow

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Run app.py when the container launches
CMD ["python", "app.py"]
