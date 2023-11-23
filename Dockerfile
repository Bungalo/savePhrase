FROM python:3.10.12

WORKDIR /app

ENV VIRTUAL_ENV = /env
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY requirements.txt .

RUN pip install -r requirements.txt
RUN apt-get -y update
RUN apt-get install ffmpeg  -y

# Copy the source code into the container.
COPY . .

# Expose the port that the application listens on.
EXPOSE 8000

# Run the application.
CMD python3 app.py
