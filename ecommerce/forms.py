from django import forms


class ContactForm(forms.Form):
    full_name = forms.CharField(
        label='Как к Вам обращаться',
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Иванов Иван"
            }
        )
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "example@example.ex"
            }
        )
    )
    content = forms.CharField(
        label='Опишите причину обращения',
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Порвало ремень генератора…"
            }
        )
    )
