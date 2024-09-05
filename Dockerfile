# Container image that runs your code
FROM python:3.9-slim

COPY *.py /

ENTRYPOINT ["python", "/main.py"]
