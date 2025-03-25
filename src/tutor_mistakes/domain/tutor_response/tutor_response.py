from __future__ import annotations

from typing import Tuple

from .prompts import TUTOR_SYSTEM_PROMPT
from .prompts import TUTOR_USER_PROMPT

from shared.base import BaseModel
from shared.base import BaseService

from infra.llm_service import OpenAIService
from infra.llm_service import OpenAIInput

from shared.models import Tutor
from shared.models import TutorMode

from shared.const import tutor_mode_mapping
from shared.const import tutor_mapping


class TutorInput(BaseModel):
    exercise: str
    correct_answer: str
    user_answer: str
    tutor: Tutor
    tutor_mode: TutorMode


class TutorOutput(BaseModel):
    response: str


class TutorService(BaseService):
    llm_service: OpenAIService

    def process(self, inputs: TutorInput) -> TutorOutput:
        (system_prompt, user_prompt) = self._promt_generate(
            inputs, *self._get_details_keys(inputs.tutor_mode, inputs.tutor)
        )
        response = self._llm_inferences(user_prompt, system_prompt)
        return TutorOutput(response=response)

    def _llm_inferences(self, user_prompt: str, system_prompt: str) -> str:
        return str(
            self.llm_service.process(
                OpenAIInput(
                    user_prompt=user_prompt,
                    system_prompt=system_prompt,
                    json_mode=False,
                )
            ).response
        )

    def _promt_generate(
        self, inputs: TutorInput, tutor_details: str, tutor_mode_details: str
    ) -> Tuple[str, str]:
        system_prompt = TUTOR_SYSTEM_PROMPT
        user_prompt = TUTOR_USER_PROMPT.format(
            exercise_prompt=inputs.exercise,
            correct_answer=inputs.correct_answer,
            user_answer=inputs.user_answer,
            mode=inputs.tutor.value,
            mode_details=tutor_details,
            explanation_type=inputs.tutor_mode,
            explanation_type_details=tutor_mode_details,
        )
        return (system_prompt, user_prompt)

    def _get_details_keys(self, tutor_mode: TutorMode, tutor: Tutor) -> Tuple[str, str]:
        tutor_details = tutor_mapping[tutor]
        tutor_mode_details = tutor_mode_mapping[tutor_mode]
        return (tutor_details.value, tutor_mode_details.value)
