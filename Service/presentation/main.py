from fastapi import FastAPI

app = FastAPI(title="Auth Service")

@app.get("/")
def root():
    return {"message": "Hello from Auth Service!"}
