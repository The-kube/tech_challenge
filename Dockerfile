FROM python:3.6-slim-buster

WORKDIR /app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

EXPOSE 6000

#RUN env FLASK_APP=flask_api.py

CMD [ "flask", "run", "--host=0.0.0.0", "--port=6000"]

#CMD ["python", "./app.py"]

#ENTRYPOINT ["python", "./app.py"]