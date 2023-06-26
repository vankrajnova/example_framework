FROM python

WORKDIR /example_framework/

VOLUME /allure_results

COPY . .

RUN pip install -r requirements.txt


CMD ["pytest", "--alluredir=./allure-results"]
