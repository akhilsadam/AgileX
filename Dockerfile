# syntax=docker/dockerfile:1

FROM ubuntu:latest

WORKDIR agilex-docker

COPY requirements.txt requirements.txt

RUN apt-get update -y && apt-get install -y python3-pip python3-dev build-essential git-all npm
RUN pip3 install -r requirements.txt
RUN npm install https://github.com/fabien0102/git2json

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]