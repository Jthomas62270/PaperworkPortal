FROM python:3.9-slim 

WORKDIR /src

COPY . /app

RUN pip install --no-cachew-dir -r -requirements.txt

EXPOSE 80 

ENV NAME World 

CMD ["python", "app.py"]