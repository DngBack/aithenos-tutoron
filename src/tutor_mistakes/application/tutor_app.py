from __future__ import annotations

from functools import cached_property

from domain.tutor_response import TutorInput
from domain.tutor_response import TutorOutput
from domain.tutor_response import TutorService

from shared.base import BaseModel
from shared.base import BaseService

from shared.models import Tutor
from shared.models import TutorMode

from infra.llm_service import OpenAIService

from shared.settings import Settings
from shared.settings import load_settings


class TutorAppInput(BaseModel):
    exercise: str
    correct_answer: str
    user_answer: str
    tutor: Tutor
    tutor_mode: TutorMode


class TutorAppOutput(BaseModel):
    response: str


class TutorAppService(BaseService):
    @cached_property
    def settings(self) -> Settings:
        return load_settings()

    @cached_property
    def openai_sevice(self) -> OpenAIService:
        return OpenAIService(settings=self.settings.openai)

    @cached_property
    def tutor_service(self) -> TutorService:
        return TutorService(llm_service=self.openai_sevice)

    def process(self, inputs: TutorAppInput) -> TutorOutput:
        response = self._interact_llm(
            inputs=TutorInput(
                exercise=inputs.exercise,
                correct_answer=inputs.correct_answer,
                user_answer=inputs.user_answer,
                tutor=inputs.tutor,
                tutor_mode=inputs.tutor_mode,
            ),
        ).response
        return TutorOutput(response=response)

    def _interact_llm(self, inputs: TutorInput) -> TutorOutput:
        return self.tutor_service.process(inputs=inputs)
