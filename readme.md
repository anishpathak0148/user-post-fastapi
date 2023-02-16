## To Start venv on Mac or Linux:
    source venv/bin/activate

## To start the server:
    uvicorn app.main:app --reload

## To generate a secure random secret key:
    openssl rand -hex 32

## To create configmap in kubernetes cluster:
    kubectl create cm user-post-config --from-env-file=./env/config.env
## To create secret in kubernetes cluster:
    kubectl create secret generic user-post-secret --from-env-file=./env/secret.env

## To access postgres inside kuberbetes pod:
    psql -h localhost -p 5432 -U postgres