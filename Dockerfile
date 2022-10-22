FROM python:3.8

RUN mkdir -p /app
COPY . /app
WORKDIR /app/ICBot

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y ffmpeg
RUN apt-get install -y wget
RUN apt-get install -y procps
RUN apt-get install -y neofetch

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

CMD python3 main.py