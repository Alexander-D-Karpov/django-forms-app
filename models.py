import secrets
import string
from datetime import datetime

from django.db import models

# Create your models here.
from django.urls import reverse

from user.models import Person


QUESTION_TYPE = [
    ("question", "question"),
    ("number", "number"),
    ("select", "select"),
]

ANSWER_TYPE = [
    ("bg-success", "success"),
    ("bg-danger", "incorrect"),
    ("bg-primary", "common"),
]


class Test(models.Model):
    name = models.CharField(max_length=50, blank=False)
    slug = models.SlugField(max_length=20, blank=True)
    creator = models.ForeignKey(Person, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="uploads/images/", blank=True)
    passed = models.IntegerField(default=0)
    time_till = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

    def available(self):
        return self.time_till.timestamp() >= datetime.now().timestamp() if self.time_till else True

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if not self.slug:
            self.slug = "".join(secrets.choice(string.ascii_letters) for _ in range(20))
        super(Test, self).save()

    class Meta:
        db_table = "Tests"
        ordering = ("-created",)

    def get_absolute_url(self):
        return reverse("test", kwargs={"slug": self.slug})


class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    required = models.BooleanField(default=True)
    type = models.CharField(choices=QUESTION_TYPE, max_length=100, blank=False)
    question = models.CharField(max_length=250, blank=False)
    help = models.CharField(max_length=200, blank=True)
    correct_answer = models.CharField(max_length=100, blank=True)

    def get_selection_list(self):
        if self.type != "select":
            return []
        return QuestionSelect.objects.filter(question=self)

    def is_multiple_select(self):
        return bool(len(QuestionSelect.objects.filter(question=self, correct=True)) - 1)

    def __str__(self):
        return self.question + " " + self.type


class Answer(models.Model):
    text = models.CharField(max_length=500)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    type = models.CharField(max_length=50, choices=ANSWER_TYPE, default="bg-primary")

    def __str__(self):
        return self.text


class Submission(models.Model):
    user = models.ForeignKey(Person, blank=True, null=True, on_delete=models.SET_NULL)
    slug = models.SlugField(blank=True, max_length=10)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    submitted = models.DateTimeField(auto_now_add=True)

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if not self.slug:
            self.slug = "".join(secrets.choice(string.ascii_letters) for _ in range(10))
        super(Submission, self).save()

    def get_answers(self):
        return AnswerInSubmission.objects.filter(submission=self)

    def __str__(self):
        return (
            self.user.username + " " + self.test.name if self.user else self.test.name
        )


class AnswerInSubmission(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

    def __str__(self):
        return self.submission.test.name + " " + self.answer.question.question


class QuestionSelect(models.Model):
    text = models.CharField(blank=False, max_length=50)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    correct = models.BooleanField(default=False)

    def get_id(self):
        return f"{self.id}_question_option"

    def get_name(self):
        return f"{self.question.id}_radio"

    def __str__(self):
        return f"{self.text} on {self.question.question}"
