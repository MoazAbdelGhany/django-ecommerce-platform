from django import forms
from .models import Account
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Account
        fields = [
            "first_name",
            "last_name",
            "email",
            "country",
            "phone_number",
        ]
    # -----------------------
    # initialization
    # -----------------------
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        for name , field in self.fields.items():
            field.widget.attrs.update({
                "class": "form-control",
                "placeholder": field.label or name.replace("_"," ").title(),
            })
        self.fields["phone_number"].widget.attrs["type"] = "tel"
        self.fields["phone_number"].widget.attrs["placeholder"] = "(201) 555-0123"
    # -----------------------
    # Field Validation 
    # -----------------------
    def clean_password(self):
        password = self.cleaned_data.get("password")
        if password:
            validate_password(password)
        return password
    # -----------------------
    # Cross-field Validation
    # -----------------------
    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password:
            if password != confirm_password:
                self.add_error("confirm_password", "Passwords do not match.")
        return cleaned_data
