from fastapi import FastAPI

import team

app = FastAPI()

app.include_router(team.router)

@app.get("/", tags=["Health"])
def root():
    return {
        "mensagem": "APP IS RUNNING"
    }
