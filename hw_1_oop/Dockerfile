FROM python:3.10

COPY requirements.txt /proj/requirements.txt

COPY FinalProject /proj
WORKDIR /proj

RUN pip install -r requirements.txt
RUN pip install Flask

ENTRYPOINT ["python3", "__main__.py"]
