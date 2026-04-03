import logging

from arq import run_worker

from app.config import settings
from app.jobs.process_record import process_record

logging.basicConfig(level=settings.LOG_LEVEL.upper())
logger = logging.getLogger(__name__)


class WorkerSettings:
    functions = [process_record]
    redis_settings = settings.redis_settings
    max_jobs = 10
    job_timeout = 300


def main():
    logger.info("Starting worker in %s mode", settings.APP_ENV)
    run_worker(WorkerSettings)  # type: ignore[arg-type]


if __name__ == "__main__":
    main()
