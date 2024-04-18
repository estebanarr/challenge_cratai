FROM python:3.9-slim

COPY requirements.txt challenge/requirements.txt
RUN pip install --no-cache-dir -r /challenge/requirements.txt

COPY ./app_web/ /challenge/app_web/

WORKDIR /challenge/app_web/

ENV PYTHONPATH=/challenge/

EXPOSE 8502

CMD ["streamlit","run","main.py","--server.port","8502"]