FROM python:3.10-alpine

WORKDIR /app

ADD Pipfile /app
ADD Pipfile.lock /app
ADD main.py /app

RUN apk update && apk upgrade && apk add bash curl git
RUN curl https://pyenv.run | bash
RUN pip install pipenv
RUN pipenv install

CMD ["pipenv", "run", "main"]
