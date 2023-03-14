

FROM ubuntu:latest 

RUN mkdir ./app
WORKDIR /app

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Kolkata
  
RUN apt -qq update && apt -qq install -y git wget pv jq python3-dev ffmpeg zip curl mediainfo
 
COPY . . 
RUN pip3 install -r requirements.txt 

CMD bash start.sh
