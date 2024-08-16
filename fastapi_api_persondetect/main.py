from fastapi import FastAPI

from routes import detection, home, login


app = FastAPI()
app.include_router(detection.router)
app.include_router(home.router)
app.include_router(login.router)


@app.get("/")
def home():  # No parentheses
    return {'message': 'Home - Detector de carros API Flask'}