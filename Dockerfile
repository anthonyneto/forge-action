FROM python:3.9-slim

COPY requirements.txt /

RUN python -m pip install --upgrade pip && \
    pip install -r requirements.txt

COPY *.py /

ENTRYPOINT ["python", "/main.py"]
