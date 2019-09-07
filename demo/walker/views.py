from django.shortcuts import render, redirect
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotFound, JsonResponse, HttpResponseBadRequest, Http404
from django.urls import reverse
from django.utils.timezone import now
from walker import models, forms
from walker import metrics


class WalkDetailsView(View):
    def get_walk(self, walk_id=None):
        try:
            return models.Walk.objects.get(id=walk_id)
        except ObjectDoesNotExist:
            raise Http404(f'no walk with ID {walk_id} in progress')


class CheckWalkStatusView(WalkDetailsView):
    def get(self, request, walk_id=None, **kwargs):
        walk = self.get_walk(walk_id=walk_id)
        return JsonResponse({'complete': walk.is_complete})


class CompleteWalkView(WalkDetailsView):
    def get(self, request, walk_id=None, **kwargs):
        walk = self.get_walk(walk_id=walk_id)
        return render(request, 'index.html', context={'form': forms.CompleteWalkForm(instance=walk)})

    def post(self, request, walk_id=None, **kwargs):
        try:
            walk = models.Walk.objects.get(id=walk_id)
        except ObjectDoesNotExist:
            return HttpResponseNotFound(content=f'no walk with ID {walk_id} found')

        if walk.is_complete:
            return HttpResponseBadRequest(content=f'walk {walk.id} is already complete')

        form = forms.CompleteWalkForm(data=request.POST, instance=walk)

        if form.is_valid():
            updated_walk = form.save(commit=False)
            updated_walk.end_time = now()
            updated_walk.save()

            metrics.walks_completed.inc()
            metrics.walk_distance.observe(updated_walk.distance)

            return redirect(f'{reverse("walk_start")}?walk={walk.id}')

        return HttpResponseBadRequest(content=f'form validation failed with errors {form.errors}')


class StartWalkView(View):
    def get(self, request):
        return render(request, 'index.html', context={'form': forms.StartWalkForm()})

    def post(self, request):
        form = forms.StartWalkForm(data=request.POST)

        if form.is_valid():
            walk = form.save(commit=False)
            walk.start_time = now()
            walk.save()

            metrics.walks_started.inc()

            return redirect(f'{reverse("walk_start")}?walk={walk.id}')

        metrics.invalid_walks.inc()

        return HttpResponseBadRequest(content=f'form validation failed with errors {form.errors}')
