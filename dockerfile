FROM python:3.8-slim

ENV PORT "80"
ENV HOST "0.0.0.0"


COPY req.txt .
RUN apt-get update && apt-get upgrade
RUN pip install --no-cache-dir --upgrade -r req.txt && apt-get install libgomp1
RUN

COPY . .

CMD ["python3","test_app/ml.py"]
# CMD ["uvicorn", "test_app.app:app", "--host", $HOST, "--port", $PORT]
