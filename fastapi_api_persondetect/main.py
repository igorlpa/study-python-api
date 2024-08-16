from fastapi import FastAPI

from routes import detection, home, login


app = FastAPI(
    title='Exemplo detector de pessoa com FastAPI',
    version='0.0.1'
    )
app.include_router(detection.router, tags=['detection'])
app.include_router(home.router, tags=['login'])
app.include_router(login.router, tags=['login'])


@app.get("/")
def home():  # No parentheses
    return {'message': 'Home - Detector de carros API Flask'}