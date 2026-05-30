from fastapi import FastAPI

app = FastAPI(title="CIS OneOps Enterprise")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/")
async def root():
    return {"message": "Welcome to CIS OneOps Enterprise API"}
