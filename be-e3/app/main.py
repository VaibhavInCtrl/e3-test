from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from app.routes import agents, drivers, conversations, test_calls

app = FastAPI(
    title="E3 Backend API",
    description="API for managing agents, drivers, and test call conversations",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"}
    )

app.include_router(agents.router)
app.include_router(drivers.router)
app.include_router(conversations.router)
app.include_router(test_calls.router)

@app.get("/")
async def root():
    return {"message": "E3 Backend API", "status": "running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

