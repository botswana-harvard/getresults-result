from django import forms
from getresults_result.models import ResultItem


class ResultSearchForm(forms.Form):

    search_term = forms.CharField(
        max_length=35,
        label="Search",
        help_text="enter all or part of a order number, sample identifier, patient identifier, etc",
        error_messages={'required': 'Please enter a search term.'},
    )


class ValidationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ValidationForm, self).__init__(*args, **kwargs)
        for k in self.fields:
            self.fields[k].label = ''
            self.fields[k].required = False
            self.fields[k].widget = forms.HiddenInput()

#     def validate_unique(self):
#         return True

    class Meta:
        model = ResultItem
        fields = '__all__'
