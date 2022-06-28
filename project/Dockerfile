# pull official base image
FROM python:3.10.4-slim-buster

# set working directory
WORKDIR /usr/src/app

# set environment variables
# Prevents Python from writing pyc files to disc
# Prevents Python from buffering stdout and stderr
ENV PYTHONDONTWRITEBYTECODE 1 
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update \
  && apt-get -y install netcat gcc postgresql\
  && apt-get clean

# install python dependencies
COPY ./requirements.txt .
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

RUN pip install -U pip setuptools wheel && pip install -U spacy\
    && python -m spacy download en_core_web_sm && python -m spacy download it_core_news_sm\
    && python -m pip install intel_extension_for_pytorch -f https://software.intel.com/ipex-whl-stable

# add app
COPY . .

# add entrypoint.sh
COPY ./entrypoint.sh .
RUN chmod +x /usr/src/app/entrypoint.sh

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
