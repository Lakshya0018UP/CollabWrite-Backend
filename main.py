from fastapi import FastAPI
from routes.auth_routes import router as auth_router
from routes.document_routes import router as doc_router
import uvicorn
import os
# 1. Create the main FastAPI application
app = FastAPI(title="Collaborative Document Editor API")


app.include_router(auth_router)
app.include_router(doc_router)
@app.get("/")
async def read_root():
    return {"message": "Welcome to the Collaborative Document API"}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)