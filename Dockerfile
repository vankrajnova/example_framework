FROM python:3.10

WORKDIR /example_framework/

VOLUME /allure-results

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD pytest -s -v tests/test_docker_and_ci.py --alluredir=allure_results