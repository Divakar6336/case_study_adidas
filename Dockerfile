Dockerfile

FROM ubuntu:22.04

RUN apt-get update && \ 
    
    apt-get -o APT:Install-Recommends=false install -y python3-pip=22.0.2+dfsg-1 &&  \
    apt-get install libgomp1 && \
    rm -fr /var/lib/apt/lists/* 

WORKDIR /home/usr/app/

COPY . .

RUN pip install --no-catch-dir -r /home/usr/app/requirements.txt 

CMD ["uvicorn", "controller.main:app", "--host", "0.0.0.0", "--port", "6098"]

EXPOSE 6098
