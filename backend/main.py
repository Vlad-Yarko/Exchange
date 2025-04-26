import uvicorn

from src import asgi_app, wsgi_app


if __name__ == '__main__':
    uvicorn.run(asgi_app)
    # wsgi_app.run(port=8000)
