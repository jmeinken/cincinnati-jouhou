from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth.hashers import (
    UNUSABLE_PASSWORD_PREFIX, identify_hasher,
)
from django.utils.html import format_html, format_html_join
from django.forms.utils import flatatt

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, HTML

from . import models


    
class ReadOnlyPasswordHashWidget(forms.Widget):
    def render(self, name, value, attrs):
        encoded = value
        final_attrs = self.build_attrs(attrs)

        if not encoded or encoded.startswith(UNUSABLE_PASSWORD_PREFIX):
            summary = mark_safe("<strong>%s</strong>" % ugettext("No password set."))
        else:
            try:
                hasher = identify_hasher(encoded)
            except ValueError:
                summary = mark_safe("<strong>%s</strong>" % ugettext(
                    "Invalid password format or unknown hashing algorithm."))
            else:
                summary = format_html_join('',
                                           "<strong>{}</strong>: {} ",
                                           ((ugettext(key), value)
                                            for key, value in hasher.safe_summary(encoded).items())
                                           )

        return format_html("<div{}>{}</div>", flatatt(final_attrs), summary)
    
class ReadOnlyPasswordHashField(forms.Field):
    widget = ReadOnlyPasswordHashWidget

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("required", False)
        super(ReadOnlyPasswordHashField, self).__init__(*args, **kwargs)

    def bound_data(self, data, initial):
        # Always return initial because the widget doesn't
        # render an input field.
        return initial

    def has_changed(self, initial, data):
        return False


class UserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    password1 = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
        widget=forms.PasswordInput,
        help_text=_("Enter the same password as above, for verification."))
    image = forms.CharField(widget=forms.HiddenInput, required=False)
    
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = False
        self.helper.layout = Layout(
            'id',
            'username',
            'email',
            'password1',
            'password2',
            HTML('{% load static %}<img id="user-image-preview" alt="user image preview" src="{% static \'img/generic_user.png\' %}" width="150" height="150" />'),
            HTML('<button type="button" class="btn btn-sm btn-default" data-toggle="modal" data-target="#add-image-modal">Add Image</button>'),
            'image'
        )
        super(UserCreationForm, self).__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = ("username","email")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    image = forms.CharField(widget=forms.HiddenInput, required=False)
    
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = False
        self.helper.layout = Layout(
            'id',
            'username',
            'email',
            HTML('{% load static %}<img id="user-image-preview" alt="user image preview" src="{% static user.profile.get_image %}" width="150" height="150" />'),
            HTML('<button type="button" class="btn btn-sm btn-default" data-toggle="modal" data-target="#add-image-modal">Change Image</button>'),
            'image'
        )
        super(UserChangeForm, self).__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = ("username","email")


        
class SetPasswordForm(forms.Form):
    """
    A form that lets a user change set their password without entering the old
    password
    """
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    new_password1 = forms.CharField(label=_("New password"),
                                    widget=forms.PasswordInput)
    new_password2 = forms.CharField(label=_("New password confirmation"),
                                    widget=forms.PasswordInput)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(SetPasswordForm, self).__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        return password2

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['new_password1'])
        if commit:
            self.user.save()
        return self.user