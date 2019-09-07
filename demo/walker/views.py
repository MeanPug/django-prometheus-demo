from django.shortcuts import render, redirect
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotFound, JsonResponse, HttpResponseBadRequest
from django.urls import reverse
from django.utils.timezone import now
from walker import models, forms


class CheckWalkStatusView(View):
    def get(self, request, walk_id=None, **kwargs):
        try:
            walk = models.Walk.objects.get(id=walk_id)
        except ObjectDoesNotExist:
            return HttpResponseNotFound(content=f'no walk with ID {walk_id} in progress')

        return JsonResponse({'complete': walk.is_complete})


class StartWalkView(View):
    def get(self, request):
        return render(request, 'index.html', context={'form': forms.StartWalkForm()})

    def post(self, request):
        form = forms.StartWalkForm(data=request.POST)

        if form.is_valid():
            walk = form.save(commit=False)
            walk.start_time = now()
            walk.save()

            return redirect(f'{reverse("walk_start")}?walk={walk.id}')

        return HttpResponseBadRequest(content=f'form validation failed with errors {form.errors}')
