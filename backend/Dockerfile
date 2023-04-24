FROM python:3.10-alpine

COPY backend/requirements.txt backend/app.py backend/.flaskenv ./
RUN pip install -r ./requirements.txt
ENV FLASK_ENV production

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]