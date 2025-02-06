if [ "$ENV" = "PROD" ]; then
    uvicorn app.main:app --port 10000
else
    uvicorn app.main:app --port 8080
fi
