FROM python:3.11
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
COPY requirements.txt /app
RUN pip install -r requirements.txt
EXPOSE 5000
COPY . /app
CMD flask run --host=0.0.0.0