from forms.models import Test
from user.models import Person


def form_list(user: Person) -> dict:
    test = Test.objects.filter(creator=user)
    return {"forms": test}
