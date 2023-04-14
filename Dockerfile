FROM python:3.11
WORKDIR /app
COPY . /app
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install -r requirements.txt
EXPOSE 5000
CMD flask run 