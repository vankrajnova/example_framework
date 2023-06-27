FROM python
ARG path=/app
ARG PROJECT='autotest'
WORKDIR $path/$PROJECT

#VOLUME /allure_results

COPY . .

RUN pip install -r requirements.txt


CMD ["pytest", "--alluredir=./allure-results"]
