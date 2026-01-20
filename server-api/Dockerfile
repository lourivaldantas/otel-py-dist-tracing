FROM python:3.12-alpine

WORKDIR /apps

COPY requirements.txt .

RUN pip install --no-cache -r requirements.txt

COPY . .

CMD [ "flask", "--app", "app.py", "run", "--host=0.0.0.0", "--port", "5000" ]
