FROM python
WORKDIR /example_framework/
COPY requirements.txt ./

RUN pip install -r requirements.txt
COPY . .

CMD ["pytest", "--alluredir=./allure-results", "tests/test_docker_and_ci.py"]
