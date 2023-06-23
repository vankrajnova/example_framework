FROM python
# WORKDIR /example_framework/
# ENV ENV=dev
# COPY requirements.txt ./


COPY . .
RUN pip install -r requirements.txt
# CMD ["pytest", "--alluredir=./allure-results", "tests/test_docker.py"]
