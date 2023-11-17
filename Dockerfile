FROM python:3.10-alpine

WORKDIR /application

COPY requirements.txt /application/

RUN pip install --no-cache-dir -r requirements.txt

COPY /src/recipeservice /application/recipeservice
COPY /app/server.py /application/server.py

EXPOSE 8443


CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "7005", "--root-path", "/recipeservice"]