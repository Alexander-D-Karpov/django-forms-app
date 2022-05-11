from django.shortcuts import get_object_or_404

from forms.models import Test


def get_test_info(slug: str) -> dict:
    test = get_object_or_404(Test, slug=slug)
    return {"test": test}
