# Use alpine as the base of our image
FROM alpine:3.10
# Add needed libraries
RUN apk add --update \
    sqlite\
    python \
    py-pip
# Set work directory
WORKDIR /app
#copy application
ADD . /app

# Install requirements.txt
RUN pip install -r app/Requirements.txt

# Setup environment variables
ENV FLASK_APP=app
ENV FLASK_ENV=production

# Expose ports
EXPOSE 5000

# Initialize db
RUN python initialize_db.py
RUN python fill_db.py

# This is what will run when we do docker run
CMD flask run --host=0.0.0.0