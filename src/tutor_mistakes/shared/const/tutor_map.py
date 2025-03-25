from __future__ import annotations

from ..models import Tutor
from ..models import TutorDetails
from ..models import TutorMode
from ..models import TutorModeDetails

tutor_mapping = {
    Tutor.HINT: TutorDetails.HINT,
    Tutor.DETAILS: TutorDetails.DETAILS,
    Tutor.ANSWER: TutorDetails.ANSWER,
}

tutor_mode_mapping = {
    TutorMode.FRIENDLY: TutorModeDetails.FRIENDLY,
    TutorMode.NORMAL: TutorModeDetails.NORMAL,
    TutorMode.GRUMPY: TutorModeDetails.GRUMPY,
    TutorMode.BOSS: TutorModeDetails.BOSS,
}
