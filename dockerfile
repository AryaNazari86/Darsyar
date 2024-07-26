FROM docker.arvancloud.ir/python:3.10.12

apk add weasyprint

apk add py3-pip gcc musl-dev python3-dev pango zlib-dev jpeg-dev openjpeg-dev g++ libffi-dev harfbuzz-subset

WORKDIR /var/www/Darsyar/app

COPY ./requirements.txt ./

RUN pip install --trusted-host mirrors.aliyun.com -i http://mirrors.aliyun.com/pypi/simple/ -r requirements.txt

COPY . .

CMD [ "python", "./manage.py", "runserver", "0.0.0.0:6969"]