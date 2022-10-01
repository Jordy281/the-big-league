FROM python:3.10-slim

ENV FLASK_APP leagues.py
ENV FLASK_ENV production

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY api api
COPY leagues.py config.py boot.sh .env ./

EXPOSE 5000
# CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0" ]
# CMD [ "python3", "-m" , "flask", "run" ]
CMD ["./boot.sh"]