from fastapi import FastAPI

app = FastAPI()

# app.include_router(jurisprudencia.router)

@app.get("/", tags=["Health"])
def root():
    return {
        "mensagem": "APP IS RUNNING"
    }
