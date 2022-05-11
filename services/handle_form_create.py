import pytz
from django.core.files.uploadedfile import InMemoryUploadedFile

from datetime import datetime

from forms.models import Test, Question, QuestionSelect
from user.models import Person


def create_form(data: dict, user: Person, question_amout: int, image: InMemoryUploadedFile = None) -> Test:
    if data["test_calendar"] and data["test_time"]:
        dt = datetime(
            year=int(data["test_calendar"].split(".")[2]),
            month=int(data["test_calendar"].split(".")[1]),
            day=int(data["test_calendar"].split(".")[0]),
            hour=int(data["test_time"].split(":")[0]),
            minute=int(data["test_time"].split(":")[1]),
            second=0,
            microsecond=0,
            tzinfo=pytz.timezone("Europe/Moscow"),
        )
    elif data["test_calendar"]:
        dt = datetime(
            year=int(data["test_calendar"].split(".")[2]),
            month=int(data["test_calendar"].split(".")[1]),
            day=int(data["test_calendar"].split(".")[0]),
            hour=0,
            minute=0,
            second=0,
            microsecond=0,
            tzinfo=pytz.timezone("Europe/Moscow"),
        )
    else:
        dt = None

    test = Test.objects.create(
        name=data["test_name"], creator=user, description=data["test_description"], image=image, time_till=dt
    )
    for i in range(1, question_amout + 1):
        if data[str(i) + "_question_type"] == "select":
            qst = Question.objects.create(
                question=data[str(i) + "_question"],
                required=bool(data[str(i) + "_question_required"]),
                type=data[str(i) + "_question_type"],
                test_id=test.id,
                help=data[str(i) + "_question_help"],
            )
            for x in data:
                if "question_option_text" in x:
                    n, el = (int(elll) for elll in x.split("_")[:2])
                    if n == i:
                        QuestionSelect.objects.create(
                            text=data[x],
                            question_id=qst.id,
                            correct=f"{i}_{el}_question_option_required" in data
                        )
        else:
            Question.objects.create(
                question=data[str(i) + "_question"],
                required=bool(data[str(i) + "_question_required"]),
                type=data[str(i) + "_question_type"],
                test_id=test.id,
                help=data[str(i) + "_question_help"],
                correct_answer=data[str(i) + "_question_answer"],
            )
    return test
