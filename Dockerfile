FROM python:3.12

WORKDIR /app

COPY team_estimator.py .

RUN pip install class-argparse

ENTRYPOINT ["/bin/bash"]
