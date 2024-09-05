# Container image that runs your code
FROM python:3.8-slim

COPY entrypoint.py /entrypoint.py

ENTRYPOINT ["/entrypoint.py"]
