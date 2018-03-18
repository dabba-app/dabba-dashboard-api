FROM python:2.7

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

RUN ls

EXPOSE 8000

CMD ["python", "app.py"]
