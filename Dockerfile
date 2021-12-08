FROM python:latest
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
EXPOSE 8000
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/