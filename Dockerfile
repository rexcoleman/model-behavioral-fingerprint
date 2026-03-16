FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir \
    numpy scipy scikit-learn matplotlib seaborn pandas \
    torch --index-url https://download.pytorch.org/whl/cpu \
    fastapi uvicorn[standard] umap-learn

COPY . .

EXPOSE 8000

CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]
