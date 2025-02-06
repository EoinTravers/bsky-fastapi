if [ -z "$PORT" ]; then
    if [ "$ENV" = "PROD" ]; then
        PORT=80
    else
        PORT=9999
    fi
fi

uvicorn app.main:app --host 0.0.0.0 --port $PORT