from django.urls import path

from forms.views import test, form, submit, result, admin, index, create, form_submit

urlpatterns = [
    path("", index, name="all_forms"),
    path("create", create, name="create_form"),
    path("create/s", form_submit, name="create_form_submit"),
    path("<str:slug>", test, name="test"),
    path("<str:slug>/t", form, name="form"),
    path("<str:slug>/s", submit, name="submit_test"),
    path("<str:slug>/a", admin, name="form_admin"),
    path("<str:slug>/<str:sub_slug>", result, name="form_result"),
]
