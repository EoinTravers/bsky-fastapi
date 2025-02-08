if [ -z "$PORT" ]; then
    if [ "$ENV" = "PROD" ]; then
        PORT=10000
    else
        PORT=9999
    fi
fi

uvicorn fastapi_app.main:app --host 0.0.0.0 --port $PORT