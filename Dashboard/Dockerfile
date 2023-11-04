FROM continuumio/miniconda3

WORKDIR /home/app

RUN apt-get update -y
RUN apt-get install nano unzip
RUN apt install curl -y

COPY requirements.txt /dependencies/requirements.txt
RUN pip install -r /dependencies/requirements.txt

COPY . .

CMD streamlit run --server.port $PORT Getaround_dashboard.py