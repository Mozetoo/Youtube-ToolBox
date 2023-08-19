from django import forms


class SearchByNameForm(forms.Form):
    search_query = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Search By Name', 'class': 'form-control col-lg-8 col-xl-6', 'style': 'width: 400px;'}),
        label='',
    )


class SearchByURLForm(forms.Form):
    url_query = forms.URLField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Search By Url', 'class': 'form-control col-lg-8 col-xl-6', 'style': 'width: 400px;'}),
        label='',
    )
