from django import forms

from catalog.models import Product, Version

FORBIDDEN_WORDS = ('казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар')


class ProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
    class Meta:
        model = Product
        fields = '__all__'

    def clean_name(self):
        cleaned_data = self.cleaned_data['name']
        if cleaned_data in FORBIDDEN_WORDS:
            raise forms.ValidationError('Запрещенное название')
        return cleaned_data

    def clean_description(self):
        cleaned_data = self.cleaned_data['description']
        if cleaned_data in FORBIDDEN_WORDS:
            raise forms.ValidationError('Запрещенное описание')
        return cleaned_data

class VersionForm(forms.ModelForm):


    is_active = forms.BooleanField(label='Признак текущей версии', required=False, widget=forms.CheckboxInput())
    class Meta:
        model = Version
        fields = '__all__'

    def clean_is_active(self):
        cleaned_data = self.cleaned_data['is_active']
        if cleaned_data and self.instance.product.version_set.filter(is_active=True).exclude(
                id=self.instance.id).exists():
            raise forms.ValidationError('Может существовать только одна активная версия.')
        return cleaned_data
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

