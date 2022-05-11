from django.shortcuts import get_object_or_404

from forms.models import Submission, AnswerInSubmission


def get_result_info(slug: str) -> dict:
    sub = get_object_or_404(Submission, slug=slug)
    answers = [x.answer for x in AnswerInSubmission.objects.filter(submission=sub)]
    return {"submission": sub, "answers": answers}
