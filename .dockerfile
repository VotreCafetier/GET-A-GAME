FROM python:3.8-slim-buster
RUN pip3 install -r requirements.txt
CMD ["python3", "./GETAGAME.py"]