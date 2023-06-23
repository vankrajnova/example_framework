FROM python
WORKDIR /example_framework/
# ENV ENV=dev
COPY requirements.txt ./

RUN pip install -r requirements.txt
COPY . .

CMD ["pytest", "--alluredir=./allure-results", "tests/test_docker.py"]
