from fastapi import FastAPI
from app.api.usuarios import cadastro
from app.database.session import Base, engine

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

Base.metadata.create_all(bind=engine)

app = FastAPI(title="EventHUB", description="API para gerenciamento de usuários e eventos", version="1.0.0")


app.include_router(cadastro)