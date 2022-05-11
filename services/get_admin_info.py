from django.shortcuts import get_object_or_404

from forms.models import Test, Submission


def get_form_admin(slug) -> dict:
    test = get_object_or_404(Test, slug=slug)
    submissions = Submission.objects.filter(test=test)
    admin = test.creator
    return {"submissions": submissions, "test": test, "admin": admin}
