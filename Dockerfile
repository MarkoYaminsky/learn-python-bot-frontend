FROM python:3.10

COPY app /opt/app/
COPY requirements.txt main.py /opt/

WORKDIR /opt

RUN pip install -r requirements.txt

CMD ["python", "main.py"]