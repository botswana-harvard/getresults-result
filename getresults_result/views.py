from django import forms
from django.views.generic import TemplateView, ListView
from django.shortcuts import get_object_or_404
from getresults_result.models import Result, ResultItem
from django.views.generic.base import RedirectView, View
from django.views.generic.edit import FormView, UpdateView
from getresults_result.forms import ValidationForm
from django.http.response import HttpResponseRedirect
from django.forms.formsets import formset_factory
from django.forms.models import modelformset_factory
from django.utils import timezone


class ResultSectionView(TemplateView):
    template_name = 'getresults_result/home.html'


class ResultView(TemplateView):

    template_name = 'getresults_result/result.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(ResultView, self).get_context_data(**kwargs)
        print(kwargs)
        result = Result.objects.get(pk=kwargs.get('pk'))
        result_item_list = ResultItem.objects.filter(result=result)
        ValidationFormset = modelformset_factory(
            model=ResultItem, form=ValidationForm, extra=0)
        context.update(
            validation_formset=ValidationFormset(queryset=result_item_list),
            order=result.order,
            section_title=kwargs.get('result_identifier'))
        return context

    def post(self, request, *args, **kwargs):
        ValidationFormset = modelformset_factory(model=ResultItem, form=ValidationForm, extra=0)
        result = Result.objects.get(pk=kwargs.get('pk'))
        result_item_list = ResultItem.objects.filter(result=result)
        if self.request.POST:
            formset = ValidationFormset(request.POST, queryset=result_item_list)
            if formset.is_valid():
                validation_datetime = timezone.now()
                objects = formset.save(commit=False)
                for obj in objects:
                    obj.validation_datetime = validation_datetime
                    obj.save()
                result.validation_status = 'validated'
                result.validation_datetime = validation_datetime
                result.save()
        return HttpResponseRedirect('/result/validate/')


class UnvalidatedResultsView(ListView):

    template_name = 'getresults_result/result_list.html'
    context_object_name = 'result_list'
    paginate_by = 5

    def get_queryset(self):
        return Result.objects.exclude(validation_status__in=['validated', 'rejected']).order_by('created')

    def get_context_data(self, **kwargs):
        context = super(UnvalidatedResultsView, self).get_context_data(**kwargs)
        context.update(
            section_title='Unvalidated Results')
        return context


class SaveValidationRedirectView(View):

    permanent = False

    def post(self, request, *args, **kwargs):
        print(**kwargs)
        return super(RedirectView, self).post(request, *args, **kwargs)


class UnreleasedResultsView(ListView):

    template_name = 'getresults_result/result_list.html'
    context_object_name = 'result_list'
    paginate_by = 5

    def get_queryset(self):
        return Result.objects.filter(validation_status='validated').exclude(
            release_status__in=['released', 'rejected']).order_by('created')

    def get_context_data(self, **kwargs):
        context = super(UnreleasedResultsView, self).get_context_data(**kwargs)
        context.update(
            section_title='Unreleased Results')
        return context
