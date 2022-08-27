## To Start venv on Mac or Linux:
    source venv/bin/activate

## To start the server:
    uvicorn app.main:app --reload

## To generate a secure random secret key:
    openssl rand -hex 32