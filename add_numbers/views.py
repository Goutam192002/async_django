from celery import current_app
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django import forms
from add_numbers.tasks import adding_task


class AddTwoNumbersForm(forms.Form):
    number_1 = forms.IntegerField(required=True)
    number_2 = forms.IntegerField(required=True)


class IndexView(View):
    def get(self, request):
        return render(request, 'add_numbers/home.html', {'form': AddTwoNumbersForm})

    def post(self, request):
        form = AddTwoNumbersForm(request.POST)
        context = {}

        if form.is_valid():
            task = adding_task.delay(int(form.data["number_1"]), int(form.data["number_2"]))
            context['task_id'] = task.id
            context['task_status'] = task.status
            return render(request, "add_numbers/home.html", context)

        context['form'] = form
        return render(request, "add_numbers/home.html", context)


class TaskView(View):
    def get(self, request, task_id):
        task = current_app.AsyncResult(task_id)
        response_data = {'task_status': task.status, 'task_id': task.id}

        if task.status == 'SUCCESS':
            response_data['results'] = task.get()

        return JsonResponse(response_data)
