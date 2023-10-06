from fastapi import FastAPI
from app.routers.user_router import router as UserRouter
from app.routers.metric_router import router as MetricRouter
from app.routers.user_metric_router import router as UserMetricRouter
from app.routers.admin_router import router as AdminRouter
from app.routers.section_router import router as SectionRouter
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware settings
origins = [
    "http://localhost:8080",  # Allow frontend origin
    # Add any other origins if needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(UserRouter, tags=["Users"], prefix="/users")
app.include_router(MetricRouter, tags=["Metrics"], prefix="/metrics")
app.include_router(SectionRouter, tags=["Sections"], prefix="/sections")
app.include_router(UserMetricRouter, tags=["User Metrics"], prefix="/user_metrics")
app.include_router(AdminRouter, tags=["Admin"], prefix="/admin")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}
