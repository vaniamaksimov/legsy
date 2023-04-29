from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from legsy.api import main_router

app = FastAPI()
app.include_router(main_router)

origins = [
    '*',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
async def test():
    return {'fastapi': 'work'}
