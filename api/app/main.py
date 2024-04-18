import uvicorn
import structlog
import uuid
import app.log_config as log_config
from starlette.requests import Request
from starlette.responses import PlainTextResponse
from fastapi import FastAPI
from app.routers import evaluate
from app.config import Settings, get_settings

logconfig_dict = log_config.read_logging_config("app/logging.yml")
log_config.setup_logging(logconfig_dict)
logger = structlog.get_logger()

structlog.configure(
        processors=[
            structlog.threadlocal.merge_threadlocal,
            structlog.stdlib.filter_by_level,
            log_config.rename_event_key,
            structlog.stdlib.add_log_level,
            structlog.stdlib.add_logger_name,
            structlog.processors.format_exc_info,
            structlog.processors.TimeStamper(key="timestamp", fmt="iso"),
            log_config.add_log_prefix_keys,
            log_config.add_log_meta_data,
            structlog.processors.JSONRenderer(),
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True
    )

app = FastAPI()

app.include_router(
    evaluate.router,
    prefix="/sustainability",
    tags=["sustainability"])


@app.exception_handler(Exception)
async def uncaught_exception_handler(request, exc):
    logger.exception("Excepcion no controlada", exception=exc)
    return PlainTextResponse(str(""), status_code=500)


@app.middleware("http")
async def add_track_id(request: Request, call_next):
    track_id = request.headers.get('TrackId', str(uuid.uuid4()))
    structlog.threadlocal.clear_threadlocal()
    structlog.threadlocal.bind_threadlocal(track_id=track_id)
    response = await call_next(request)
    structlog.threadlocal.clear_threadlocal()
    return response


@app.get("/test")
async def read_root():
    logger.debug("Received call to test")
    try:
        vers = open("app/version.txt", "r").readline()
    except FileNotFoundError:
        try:
            vers = open("version.txt", "r").readline()
        except FileNotFoundError:
            vers = "Version unknown"
    return vers


@app.get("/settings")
async def read_root() -> Settings:
    logger.debug("Requested settings")
    return get_settings()

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8005)
