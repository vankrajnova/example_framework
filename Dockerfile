FROM python:3.10

WORKDIR /example_framework/

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD pytest --alluredir=allure-results