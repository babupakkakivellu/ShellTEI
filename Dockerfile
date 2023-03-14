FROM ubuntu:latest 

RUN mkdir ./app
WORKDIR /app

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Kolkata
  
RUN apt -qq update && apt -qq install -y git wget pv jq python3-dev ffmpeg zip curl mediainfo

RUN apt -qq install -y python3-pip

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD bash start.sh
