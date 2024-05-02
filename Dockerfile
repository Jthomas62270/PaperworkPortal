FROM continuumio/anaconda3

WORKDIR /src

COPY . /app

RUN conda install --file requirements.txt

EXPOSE 80 

ENV NAME World 

CMD ["python", "app.py"]