
from schema.schemas import  Login, LoginOut
from src.authentication import sign_jwt
from fastapi import APIRouter

router = APIRouter(prefix='/login')

@router.post("/", response_model=LoginOut)
def login(login:Login):
    secret_key = login.secret_key
    
    return sign_jwt(secret_key=secret_key)

    

@router.get("/help")
def help():
    return "This is a help page for the login endpoint. \n Send the secret key to get the acitve token via JSON in field 'secret-key' "

