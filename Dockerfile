# syntax=docker/dockerfile:1

FROM python:3.8.1

WORKDIR agilex-docker

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt
RUN npm install https://github.com/fabien0102/git2json

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]