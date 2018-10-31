FROM python:3

RUN mkdir /code
WORKDIR /code

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./
RUN python ./initialization.py

CMD [ "python", "./main.py" ]
