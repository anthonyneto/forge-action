# Container image that runs your code
FROM python:3.9-slim

COPY main.py .
COPY modules/* .

ENTRYPOINT ["main.py"]
