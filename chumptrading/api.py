from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI(title='Trade Monkey')


class Message(BaseModel):
    message: str


@app.post('/chat')
def chat():
    return Message(message='Hi')
