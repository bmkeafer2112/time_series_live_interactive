FROM python:3.11.6


WORKDIR /app
COPY index.py /app

RUN pip install flask==3.0.0
RUN pip install plotly==5.18.0
RUN pip install dash==2.14.1
RUN pip install dash-bootstrap-components==1.5.0
RUN pip install dash-daq==0.5.0
RUN pip install pandas==1.5.2

EXPOSE 8055
CMD ["python", "index.py"]