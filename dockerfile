FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# WeasyPrint needs Pango/Cairo at runtime; fontconfig so it can see Vazirmatn.
RUN apt-get update && apt-get install -y --no-install-recommends \
        libpango-1.0-0 \
        libpangoft2-1.0-0 \
        libharfbuzz0b \
        libcairo2 \
        fontconfig \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# ---- Only the fonts the exam PDFs actually use ----
COPY static/fonts/Vazirmatn-*.ttf /usr/local/share/fonts/vazirmatn/
RUN fc-cache -f

COPY . .

RUN DJANGO_SECRET_KEY=build-only python manage.py collectstatic --noinput

EXPOSE 6868

# Long timeout because the /scraper/ endpoints run synchronously in-request.
CMD ["sh", "-c", "python manage.py migrate --noinput && exec gunicorn Darsyar.wsgi:application --bind ${GUNICORN_BIND:-0.0.0.0:6868} --workers 3 --timeout 600 --access-logfile - --error-logfile -"]
