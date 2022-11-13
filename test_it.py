import random

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()

origins = [    
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/test_endpoint")
def js_endpoint(input: str):
    print(input)
    return {'hello': random.randint(0,100)}

@app.get("/all_artists")
def get_all_artists():
    return ['Caravaggio', 'Duerer']

if __name__ == "__main__":
    uvicorn.run("test_it:app", host="0.0.0.0", port=8000, reload=True)
