FROM python

WORKDIR /example_framework/

VOLUME /allure_results

COPY . .

RUN pip install -r requirements.txt


CMD pytest -s -v tests/test_docker_and_ci.py --alluredir=allure-results
