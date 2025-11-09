FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    sqlite3

RUN pip install mlflow

CMD ["/bin/bash"]
