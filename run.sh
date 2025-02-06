if [ "$ENV" = "PROD" ]; then
    uvicorn app.main:app --port 80
else
    uvicorn app.main:app --port 9999
fi
