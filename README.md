# Exchange API
***
## This api is used for getting the latest prices of different currencies, making subscriptions etc
## I'll leave a tutorial for project installation bellow
## In the code for every endpoint in api I have detailed doc with different responses. Also you can It all test in swagger
***
So to get started with the project we need to do several things in different services  
You need to have postgres, redis, openssl installed on your pc  
In postgres you need to create database named "exchange"
After you installed redis you can run it locally on 6379 port
***
Okay once you do actions above you can create your .env file in "backend" folder by "example-env.txt" (commented lines you do not need)
Of course you also need to have .pem keys to hex jwt tokens
```commandline
openssl genpkey -algorithm RSA -out src/api/keys/private_key.pem
```
```commandline
openssl genpkey -algorithm RSA -out src/api/keys/public_key.pem
```
After creating .env file and keys in correct way you can do commands in shell that you can see below
```commandline
poetry install
```
```commandline
poetry run alembic upgrade head
```
```commandline
poetry run python -m src.databases.requests.fill
```
To run the api:
```commandline
poetry run python main.py
```
