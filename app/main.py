from fastapi import FastAPI
from app.routes import CandidateRoutes, HealthCheck, ReportRoutes, SearchCandidatesRoutes, UserRoutes

app = FastAPI()

app.include_router(UserRoutes.router)
app.include_router(CandidateRoutes.router)
app.include_router(HealthCheck.router)
app.include_router(ReportRoutes.router)
app.include_router(SearchCandidatesRoutes.router)