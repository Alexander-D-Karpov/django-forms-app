from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from forms.services.get_admin_info import get_form_admin
from forms.services.get_forms import form_list
from forms.services.get_questions import get_info
from forms.services.get_result_info import get_result_info
from forms.services.get_test_info import get_test_info
from forms.services.handle_answers import handle_test
from forms.services.handle_form_create import create_form


def test(request, slug):
    return render(request, "forms/test.html", get_test_info(slug))


def form(request, slug):
    return render(request, "forms/form.html", get_info(slug))


def result(request, slug, sub_slug):
    return render(request, "forms/result.html", get_result_info(sub_slug))


def index(request):
    if not request.user.is_authenticated:
        return redirect("login")
    return render(request, "forms/list.html", form_list(request.user))


def create(request):
    if not request.user.is_authenticated:
        return redirect("login")
    return render(request, "forms/create.html")


def form_submit(request):
    if request.method == "POST":
        dat_n = [x for x in request.POST if x != "csrfmiddlewaretoken"]
        data_dict = {}
        index_list = []

        # parse info into dict
        for x in dat_n:
            if "test_" not in x:
                ind = int(x.split("_")[0])
                index_list.append(ind)
            data_dict[x] = request.POST[x]
        index_list.sort()
        max_el = index_list[-1]

        # add info that question is not required
        for x in range(1, max_el + 1):
            if f"{x}_question_required" not in data_dict:
                data_dict[f"{x}_question_required"] = False

        image = request.FILES["test_image"] if "test_image" in request.FILES else None
        test = create_form(data_dict, request.user, max_el, image)
        return redirect("test", slug=test.slug)
    return redirect("create_form")


def admin(request, slug):
    if request.user.is_authenticated:
        dat = get_form_admin(slug)
        if dat["admin"] == request.user:
            return render(request, "forms/admin.html", context=dat)
    return redirect("test", slug=slug)


@require_http_methods(["POST"])
def submit(request, slug):
    data_dict = {}
    for key in request.POST:
        if "select" in key:
            data_dict[key] = list(request.POST.getlist(key))
        elif key != "csrfmiddlewaretoken":
            data_dict[key] = request.POST.get(key)

    subm = (
        handle_test(slug, data_dict, request.user)
        if request.user.is_authenticated
        else handle_test(slug, data_dict)
            )
    if subm:
        return redirect("form_result", slug=slug, sub_slug=subm.slug)
    else:
        return redirect("form", slug=slug)
