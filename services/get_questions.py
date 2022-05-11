from forms.models import Question
from forms.services.get_test_info import get_test_info


def get_questions(slug: str) -> list[Question]:
    return Question.objects.filter(test__slug=slug)


def get_info(slug: str) -> dict:
    dct = {"questions": get_questions(slug)}
    dct.update(get_test_info(slug))
    return dct
