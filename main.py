from fastapi import FastAPI
from src.categorization import categorizationRouter
from src.dialog import dialogRouter
from src.polisher import polisherRouter
import uvicorn


app = FastAPI()

app.include_router(categorizationRouter.router)
app.include_router(dialogRouter.router)
app.include_router(polisherRouter.router)


if __name__ == "__main__":
    uvicorn.run("main:app", host=8000)