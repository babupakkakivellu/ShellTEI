FROM python:3.9.2-slim-buster  
RUN chmod 777 ./ 
RUN apt -qq update && apt -qq install -y git wget pv jq python3-dev ffmpeg zip curl mediainfo  
 
COPY . . 
RUN pip3 install -r requirements.txt 
CMD ["bash","run.sh"]
