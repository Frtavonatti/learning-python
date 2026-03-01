from fastapi import FastAPI

from app.routers import posts

app = FastAPI(title="Blog API - FastAPI Tutorial")


@app.get("/")
async def root():
    return {"message": "Blog API running"}


app.include_router(posts.router)
