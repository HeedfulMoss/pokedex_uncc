FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Make sure the types directory is available
RUN mkdir -p types

EXPOSE 8501

CMD ["streamlit", "run", "pokedex_frontend.py", "--server.port=8501", "--server.address=0.0.0.0"]
