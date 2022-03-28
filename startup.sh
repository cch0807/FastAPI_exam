MAIN_PATH=app.main
BIND_ADDRESS= 0.0.0.0
PORT=8000

echo alembic upgrade head
poetry run alembic upgrade head
if [$? -ne 0]; then
    echo Failed alembic...
    exit -1

fi

echo Starting uvicorn...
poetry run uvicorn -- host ${BIND_ADDRESS} --port ${PORT} ${MAIN_PATH}:app --reload