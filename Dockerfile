FROM python
WORKDIR /example_framework/

COPY . .

RUN pip install -r requirements.txt


CMD pytest -s -v tests/test_docker_and_ci.py
