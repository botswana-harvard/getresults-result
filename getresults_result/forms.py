from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Button, Layout, Field
from django import forms
from django.forms.widgets import HiddenInput
from getresults_result.models import ResultItem, Release


class NavButtonsFormActions(FormActions):

    def __init__(self, form_id):
        super(NavButtonsFormActions, self).__init__(
            Button('previous', '<< Previous', css_class='btn-default',
                   onclick="func_previous(\'{}\');".format(form_id)),
            Button('cancel', 'Cancel', css_class='btn-default',
                   onclick="func_cancel(\'{}\');".format(form_id)),
            Button('save', 'Save', css_class='btn-default',
                   onclick="func_save(\'{}\');".format(form_id),
                   disabled=True),
            Button('savenext', 'Save and Next >>', css_class='btn-default',
                   onclick="func_savenext(\'{}\');".format(form_id),
                   disabled=True),
            Button('next', 'Next >>', css_class='btn-default',
                   onclick="func_next(\'{}\');".format(form_id)),
        )


class ResultSearchForm(forms.Form):

    search_term = forms.CharField(
        max_length=35,
        label="Search",
        help_text="enter all or part of a order number, sample identifier, patient identifier, etc",
        error_messages={'required': 'Please enter a search term.'},
    )


class NavigationForm(forms.Form):

    navigation = forms.CharField(widget=HiddenInput(), required=False)

    def __init__(self, *args, **kwargs):
        super(NavigationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.disable_csrf = True

    class Meta:
        fields = '__all__'


class ValidationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ValidationForm, self).__init__(*args, **kwargs)
        for k in self.fields:
            self.fields[k].label = ''
            self.fields[k].required = False
            self.fields[k].widget = forms.HiddenInput()
        self.fields['comment'].widget = forms.TextInput()
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.form_tag = False
        self.helper.form_id = 'id_validation_form'
        self.helper.layout = Layout(
            FormActions(
                Button('accept_all', 'Accept All', css_class='btn-default',
                       onclick='func_accept_all(\"{form_id}\");'.format(form_id=self.helper.form_id)),
                Button('repeat_all', 'Repeat All', css_class='btn-default',
                       onclick='func_repeat_all(\"{form_id}\");'.format(form_id=self.helper.form_id)),
                Button('cancel_all', 'Cancel All', css_class='btn-default',
                       onclick='func_cancel_all(\"{form_id}\");'.format(form_id=self.helper.form_id)),
                Button('ignore_all', 'Ignore All', css_class='btn-default',
                       onclick='func_ignore_all(\"{form_id}\");'.format(form_id=self.helper.form_id)),
                Button('reset_all', 'Reset', css_class='btn-default',
                       onclick='func_reset_all(\"{form_id}\");'.format(form_id=self.helper.form_id)),
            ),
            NavButtonsFormActions(form_id=self.helper.form_id),
        )

    class Meta:
        model = ResultItem
        fields = '__all__'


class ReleaseForm(forms.ModelForm):

    status = forms.CharField(widget=HiddenInput(), required=False)

    navigation = forms.CharField(widget=HiddenInput(), required=False)

    class Meta:
        model = Release
        fields = ['result', 'status', 'comment', 'navigation']

    def __init__(self, *args, **kwargs):
        super(ReleaseForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'POST'
        self.helper.form_id = 'id_release_form'
        self.helper.layout = Layout(
            Field('comment', autocomplete='off'),
            FormActions(
                Button('release', 'Release', css_class='btn-default', onclick="func_release();"),
                Button('review', 'Review', css_class='btn-default', onclick="func_review();"),
            ),
            NavButtonsFormActions(form_id=self.helper.form_id),
        )
