FROM python:3.12

RUN pip install pipenv

WORKDIR /app

COPY . .

RUN pipenv install

ENTRYPOINT ["/bin/bash"]
