FROM python:3.8-slim-buster
ADD . /app
WORKDIR /app
RUN pip install pip==20.2.2
RUN pip install -r requirements.txt
CMD  ["tail", "-f", "/dev/null"]
