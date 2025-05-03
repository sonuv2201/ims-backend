
FROM python:3.9


WORKDIR /app


COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt


COPY . .


EXPOSE 80


CMD ["gunicorn", "--bind", "0.0.0.0:80", "nish_react_lcnc_backend.wsgi:application"]





