from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404

from forms.models import Answer, Submission, Test, Question, AnswerInSubmission
from user.models import Person


def _validate(answer, typeOf) -> bool:
    if not answer:
        return True

    if typeOf == "question":
        return True
    elif typeOf == "number":
        try:
            float(answer)
        except ValueError:
            return False
        return True
    elif typeOf == "select":
        return True
    return False


def _get_answers_list(lst: list[tuple]) -> list[Answer]:
    re = []
    for el_id, el in lst:
        question = Question.objects.get(id=el_id)
        if question.correct_answer:
            if question.correct_answer.upper() == el.upper():
                tp = "bg-success"
            else:
                tp = "bg-danger"
        else:
            tp = "bg-primary"

        awns = Answer.objects.create(text=el, question=question, type=tp)
        re.append(awns)
    return re


def handle_test(slug: str, lst: list[tuple], user: Person = None) -> Submission:
    test = get_object_or_404(Test, slug=slug)
    test.passed += 1
    test.save(update_fields=["passed"])
    answers = _get_answers_list(lst)
    questions_given_req = [x.question for x in answers if _validate(x.text, x.question.type)]
    questions_req = [
        x for x in Question.objects.filter(test=test).exclude(required=False)
    ]
    if not all([item in questions_given_req for item in questions_req]):
        raise ValidationError(message="Not all questions were submitted or submitted incorrectly")

    submission = Submission.objects.create(user=user, test=test)
    for el in answers:
        AnswerInSubmission.objects.create(submission=submission, answer=el)

    return submission
