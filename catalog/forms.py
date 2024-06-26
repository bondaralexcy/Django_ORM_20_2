from django import forms
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from catalog.models import Product, Version


class StyleFormMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs["class"] = "form-control"


class ProductForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        exclude = ("owner",)

    def clean_name(self):
        cleaned_data = self.cleaned_data["name"]
        forbidden_words = [
            "казино",
            "криптовалюта",
            "крипта",
            "биржа",
            "дешево",
            "бесплатно",
            "обман",
            "полиция",
            "радар",
        ]
        for word in forbidden_words:
            if word in cleaned_data.lower():
                raise forms.ValidationError("Недопустимое слово в названии товара")

        return cleaned_data

    def clean_description(self):
        cleaned_data = self.cleaned_data["description"]
        forbidden_words = [
            "казино",
            "криптовалюта",
            "крипта",
            "биржа",
            "дешево",
            "бесплатно",
            "обман",
            "полиция",
            "радар",
        ]
        for word in forbidden_words:
            if word in cleaned_data.lower():
                raise forms.ValidationError("Недопустимое слово в описании товара")

        return cleaned_data


class ProductModeratorForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        fields = ("description", "category", "is_published")



    def clean_description(self):
        cleaned_data = self.cleaned_data["description"]
        forbidden_words = [
            "казино",
            "криптовалюта",
            "крипта",
            "биржа",
            "дешево",
            "бесплатно",
            "обман",
            "полиция",
            "радар",
        ]
        for word in forbidden_words:
            if word in cleaned_data.lower():
                raise forms.ValidationError("Недопустимое слово в описании товара")

        return cleaned_data



class VersionForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Version
        fields = "__all__"


class VersionFormset(BaseInlineFormSet):

    def clean(self):
        active_count = 0
        for form in self.forms:
            if form.cleaned_data.get("is_activе"):
                active_count += 1
        if active_count > 1:
            raise ValidationError("Может существовать только одна активная версия")
        super().clean()
