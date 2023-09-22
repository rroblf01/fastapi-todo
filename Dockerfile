FROM python:3.9-alpine

WORKDIR /code

COPY . /code

RUN apk add --no-cache --update npm

RUN cd src/tailwindcss && npm install && cd ../..

RUN pip install -r /code/requirements.txt

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]
