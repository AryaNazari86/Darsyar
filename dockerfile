FROM docker.arvancloud.ir/python:3.10.12-alpine

RUN apk add weasyprint

WORKDIR /var/www/Darsyar/app

COPY ./requirements.txt ./

RUN pip install --trusted-host mirrors.aliyun.com -i http://mirrors.aliyun.com/pypi/simple/ -r requirements.txt

# ---- WeasyPrint / Pango runtime deps (minimal) ----
RUN apt-get update && apt-get install -y --no-install-recommends \
    fontconfig \
    libpango-1.0-0 \
    libcairo2 \
 && rm -rf /var/lib/apt/lists/*

# ---- Install ONLY the fonts you use (Vazirmatn) ----
COPY static/fonts/Vazirmatn-*.ttf /usr/local/share/fonts/vazirmatn/

# ---- Build font cache so Pango can see them ----
RUN fc-cache -f

COPY . .

CMD [ "python", "./manage.py", "runserver", "0.0.0.0:6868"]