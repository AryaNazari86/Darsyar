FROM docker.arvancloud.ir/python:3.10.12-alpine

RUN apk add weasyprint

WORKDIR /var/www/Darsyar/app

COPY ./requirements.txt ./

RUN pip install --trusted-host mirrors.aliyun.com -i http://mirrors.aliyun.com/pypi/simple/ -r requirements.txt

COPY . .

CMD [ "python", "./manage.py", "runserver", "0.0.0.0:6868"]