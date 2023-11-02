FROM continuumio/miniconda3

WORKDIR /home/app

COPY requirements.txt /dependencies/requirements.txt
RUN pip install -r /dependencies/requirements.txt

COPY . .

CMD streamlit run "Home.py" 