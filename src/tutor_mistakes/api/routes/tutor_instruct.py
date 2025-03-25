from __future__ import annotations

from api.helpers.exception_handler import ExceptionHandler
from api.helpers.exception_handler import ResponseMessage
from application import TutorAppInput
from application import TutorAppService
from shared.models import Tutor
from shared.models import TutorMode
from fastapi import APIRouter
from fastapi import status
from shared.logging import get_logger

tutoron = APIRouter(prefix="/v1")
logger = get_logger(__name__)


@tutoron.post(
    "/tutoron",
    response_model=str,
    tags=["tutoron"],
    responses={
        status.HTTP_200_OK: {
            "content": {},
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: ExceptionHandler.create_response_message(  # type: ignore
            ResponseMessage.INTERNAL_SERVER_ERROR,
        ),
        status.HTTP_400_BAD_REQUEST: ExceptionHandler.create_response_message(
            ResponseMessage.BAD_REQUEST,
        ),
        status.HTTP_401_UNAUTHORIZED: ExceptionHandler.create_response_message(
            ResponseMessage.INVALID_API_KEY,
        ),
        status.HTTP_402_PAYMENT_REQUIRED: ExceptionHandler.create_response_message(  # type: ignore
            ResponseMessage.UNPROCESSABLE_ENTITY,
        ),
    },
)
async def send_questions_answer(
    exercise: str,
    correct_answer: str,
    user_answer: str,
    tutor: Tutor,
    tutor_mode: TutorMode,
):
    exception_handler = ExceptionHandler(
        logger=logger.bind(),
        service_name="tutoron",
    )

    try:
        docs_sync_process = TutorAppService()
        response = docs_sync_process.process(
            inputs=TutorAppInput(
                exercise=exercise,
                correct_answer=correct_answer,
                user_answer=user_answer,
                tutor=tutor,
                tutor_mode=tutor_mode,
            ),
        )
        return response.response

    except Exception:
        return exception_handler.handle_exception(
            message=ResponseMessage.INTERNAL_SERVER_ERROR,
            extra={"Check input against": "Inputs"},
        )


@tutoron.get("/healthz", tags=["tutoron"])
async def healthz():
    return {"status": "ok"}
