from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.forms.models import modelformset_factory
from django.forms.widgets import HiddenInput
from django.http.response import HttpResponseRedirect
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.generic import TemplateView, ListView
from django.views.generic import View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import CreateView

from .forms import ValidationForm, ReleaseForm, NavigationForm
from .models import Result, ResultItem, Release
from getresults_result.constants import ACCEPT, REPEAT, IGNORE, CANCEL, NEXT, PREVIOUS, SAVENEXT


class LoginMixin(object):

    @method_decorator(login_required)
    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super(LoginMixin, self).dispatch(*args, **kwargs)


class FilterMixin(object):

    allowed_filters = {}
    allowed_excludes = {}

    def get_queryset_filters(self):
        filters = {}
        for item in self.allowed_filters:
            if item in self.request.GET:
                filters[self.allowed_filters[item]] = self.request.GET[item]
        return filters

    def get_queryset_excludes(self):
        filters = {}
        for item in self.allowed_excludes:
            if item in self.request.GET:
                filters[self.allowed_filters[item]] = self.request.GET[item]
        return filters

    def get_queryset(self):
        return super(FilterMixin, self).get_queryset().filter(
            **self.get_queryset_filters()).exclude(**self.get_queryset_excludes())


class NavigationUrlMixin(object):

    section_title = None
    list_view_url = None
    single_object_url = None

    def get_navigation(self):
        navigation = None
        navigation_form = NavigationForm(self.request.POST)
        if navigation_form.is_valid():
            navigation = navigation_form.cleaned_data.get('navigation')
        return navigation

    def get_context_data(self, **kwargs):
        context = super(NavigationUrlMixin, self).get_context_data(**kwargs)
        context['navigation_form'] = NavigationForm()
        return context

    def get_success_url(self, navigation=None):
        """Returns the next, previous or the list view url."""
        navigation = navigation or self.get_navigation()
        if navigation in [NEXT, SAVENEXT]:
            return self.get_next_url()
        elif navigation == PREVIOUS:
            return self.get_previous_url()
        return reverse(self.list_view_url)

    def get_previous_url(self):
        """Returns a url to the previous unreleased result pk, if one exists."""
        for obj in self.previous_queryset():
            return reverse(
                self.single_object_url,
                kwargs={'section_title': self.section_title, 'pk': str(obj.pk)})
        return reverse(self.list_view_url)

    def get_next_url(self):
        """Returns a url to the next unreleased result pk, if one exists."""
        for obj in self.next_queryset():
            return reverse(
                self.single_object_url,
                kwargs={'section_title': self.section_title, 'pk': str(obj.pk)})
        return reverse(self.list_view_url)

    def previous_queryset(self):
        return []

    def next_queryset(self):
        return []


class ResultSectionView(LoginMixin, TemplateView):
    template_name = 'getresults_result/home.html'


class BaseResultListView(LoginMixin, ListView, FilterMixin):

    template_name = 'getresults_result/result_list.html'
    model = Result
    context_object_name = 'result_list'
    paginate_by = 5
    allowed_filters = {
        'search': 'result_identifier__icontains'}


class UnvalidatedResultsView(BaseResultListView):

    def get_queryset(self):
        return self.model.objects.unvalidated().filter(**self.get_queryset_filters())

    def get_context_data(self, **kwargs):
        context = super(UnvalidatedResultsView, self).get_context_data(**kwargs)
        context.update(
            section_title='Results to be validated')
        return context


class UnreleasedResultsView(BaseResultListView):

    def get_queryset(self):
        return self.model.objects.unreleased().filter(**self.get_queryset_filters())

    def get_context_data(self, **kwargs):
        context = super(UnreleasedResultsView, self).get_context_data(**kwargs)
        context.update(
            section_title='Results to be released')
        return context


class BaseResultHistoryView(BaseResultListView):

    def get_context_data(self, **kwargs):
        context = super(BaseResultHistoryView, self).get_context_data(**kwargs)
        context.update(
            section_title='{} Results'.format(self.kwargs.get('section_title')))
        return context


class ResultReleaseHistoryView(BaseResultHistoryView):

    def get_queryset(self):
        return self.model.objects.released().filter(**self.get_queryset_filters()).order_by(
            '-release_datetime', 'result_identifier')


class ResultValidateView(LoginMixin, NavigationUrlMixin, TemplateView):

    template_name = 'getresults_result/result_validation.html'
    paginate_by = 5
    success_message = 'Result {result_identifier} was successfully set to \'{validation_status}\''
    section_title = 'unvalidated'
    list_view_url = 'unvalidated_results_url'
    single_object_url = 'validated_result_url'
    inline_model = ResultItem
    inline_form_class = ValidationForm
    result = None

    def get_context_data(self, formset=None, **kwargs):
        context = super(ResultValidateView, self).get_context_data(**kwargs)
        context.update(
            validation_formset=formset or self.get_formset(queryset=self.get_queryset()),
            order=self.result.order,
            section_title='{}: {}'.format(
                kwargs.get('section_title'), self.result.order.order_identifier),
            validation_form=ValidationForm(),
            accept_label=ACCEPT,
            repeat_label=REPEAT,
            cancel_label=CANCEL,
            ignore_label=IGNORE)
        return context

    def get(self, request, *args, **kwargs):
        self.result = Result.objects.get(pk=kwargs.get('pk'))
        return super(ResultValidateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.result = Result.objects.get(pk=kwargs.get('pk'))
        if self.request.POST:
            formset = self.get_formset(request.POST, queryset=self.get_queryset())
            if formset.is_valid():
                return self.formset_valid(formset, **kwargs)
            return self.formset_invalid(formset, **kwargs)
        return self.render_to_response(self.get_context_data(*args, **kwargs))

    def get_queryset(self):
        return self.inline_model.objects.filter(
            result=self.result).order_by('result__order__order_panel__name')

    def get_formset(self, *args, **kwargs):
        formset_class = modelformset_factory(model=self.inline_model, form=self.inline_form_class, extra=0)
        return formset_class(*args, **kwargs)

    def formset_valid(self, formset, **kwargs):
        navigation = kwargs.get('navigation')
        if navigation in [NEXT, PREVIOUS]:
            return HttpResponseRedirect(self.get_success_url(navigation))
        validation_datetime = timezone.now()
        result_items = formset.save(commit=False)
        for result_item in result_items:
            result_item.validation_datetime = validation_datetime
            result_item.save()
        self.result.validation_status = self.result.get_validation_status(result_items)
        self.result.validation_datetime = validation_datetime
        self.result.save()
        return HttpResponseRedirect(self.get_success_url(navigation))

    def formset_invalid(self, formset, **kwargs):
        return self.render_to_response(self.get_context_data(formset=formset, **kwargs))

    def previous_queryset(self):
        return Result.objects.unvalidated_previous(self.result.created)

    def next_queryset(self):
        return Result.objects.unvalidated_next(self.result.created)


class ReleaseDetailView(SingleObjectMixin, BaseResultListView):

    paginate_by = 30
    template_name = "getresults_result/result_release.html"
    model = Result

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Result.objects.all())
        return super(ReleaseDetailView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ReleaseDetailView, self).get_context_data(**kwargs)
        context['result'] = self.object
        form = ReleaseForm(initial=dict(result=self.object))
        form.fields['result'].widget = HiddenInput()
        form.helper.form_action = self.request.path
        context['form'] = form
        return context

    def get_queryset(self):
        return self.object.resultitem_set.all()


class ReleaseFormView(LoginMixin, NavigationUrlMixin, CreateView):

    template_name = "getresults_result/result_detail.html"
    form_class = ReleaseForm
    model = Release
    section_title = 'unreleased'
    list_view_url = 'unreleased_results_url'
    single_object_url = 'released_result_url'

    def get_form(self, form_class=None):
        form = super(ReleaseFormView, self).get_form(form_class)
        form.fields['result'].widget = HiddenInput()
        form.helper.form_action = self.request.path
        return form

    def form_valid(self, form):
        navigation = form.cleaned_data.get('navigation')
        if navigation in [NEXT, PREVIOUS]:
            self.object = form.save(commit=False)
            return HttpResponseRedirect(self.get_success_url(navigation))
        self.object = form.save()
        self.object.update_result()
        return HttpResponseRedirect(self.get_success_url(navigation))

    def previous_queryset(self):
        return Result.objects.unreleased_previous(self.object.result.validation_datetime)

    def next_queryset(self):
        return Result.objects.unreleased_next(self.object.result.validation_datetime)


class ResultReleaseView(LoginMixin, View):

    def get(self, request, *args, **kwargs):
        view = ReleaseDetailView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = ReleaseFormView.as_view()
        return view(request, *args, **kwargs)
