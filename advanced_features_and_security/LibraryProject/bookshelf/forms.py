from django import forms

class BookSearchForm(forms.Form):
    # SECURITY: Input validation prevents malicious input
    query = forms.CharField(
        max_length=100,
        required=False,
        strip=True
    )