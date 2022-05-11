from django.contrib import admin

# Register your models here.
from forms.models import Test, Question, Answer, Submission, AnswerInSubmission, QuestionSelect

admin.site.register(Test)
admin.site.register(Question)
admin.site.register(QuestionSelect)
admin.site.register(Answer)
admin.site.register(Submission)
admin.site.register(AnswerInSubmission)
