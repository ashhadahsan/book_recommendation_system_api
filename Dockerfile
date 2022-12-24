# Set base image (host OS)
FROM ubuntu:22.04


RUN apt-get update -y
RUN apt-get install -y python3
RUN apt-get install -y python3-pip

# By default, listen on port 5000
EXPOSE 5000/tcp

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt  .
COPY database.db .
COPY recommendation_results.json .



RUN pip3 install --upgrade pip


# Install any dependencies
RUN pip3 install -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY app.py .

# Specify the command to run on container start
CMD [ "python3", "./app.py" ]
