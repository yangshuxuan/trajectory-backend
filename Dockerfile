# Dockerfile - this is a comment. Delete me if you want.
FROM python:3.8.3
RUN pip install --upgrade pip
COPY . /app
WORKDIR /app
ENV nyc postgresql://postgres:123456@host.docker.internal:5432/nyc
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]