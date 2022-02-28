from django import forms
from django.core import validators
from lists.models import List
class Create(forms.Form):
    title = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'enter your title'}),
        label='title',
        validators=[
            validators.MaxLengthValidator(limit_value=50,
                                          message='تعداد کاراکترهای وارد شده نمیتواند بیشتر از 50 باشد'),
            validators.MinLengthValidator(2, 'تعداد کاراکترهای وارد شده نمیتواند کمتر از 2 باشد')
        ]
    )
    
    descriptions = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'enter your descriptions'}),
        label='descriptions',
        validators=[
            validators.MaxLengthValidator(limit_value=500,
                                          message='تعداد کاراکترهای وارد شده نمیتواند بیشتر از 50 باشد'),
            validators.MinLengthValidator(2, 'تعداد کاراکترهای وارد شده نمیتواند کمتر از 2 باشد')
        ]
    )
    
    initial_price = forms.IntegerField(label='initial price')
    
    image_url = forms.URLField(label='image url')

    def clean_title(self):
        title = self.cleaned_data.get('title')
        title_exists = List.objects.filter(title=title).exists()
        if title_exists:
            raise forms.ValidationError('title is exists')
        return title

    
