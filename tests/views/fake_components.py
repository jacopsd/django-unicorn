from datetime import datetime
from typing import Dict

from django import forms
from django.contrib import messages
from django.forms import ValidationError
from django.shortcuts import redirect

from django_unicorn.components import (
    HashUpdate,
    LocationUpdate,
    PollUpdate,
    UnicornView,
)
from example.coffee.models import Flavor


class FakeComponent(UnicornView):
    template_name = "templates/test_component.html"
    dictionary = {"name": "test"}
    method_count = 0
    check = False
    nested = {"check": False, "another": {"bool": False}}
    method_arg = ""

    def test_method(self):
        self.method_count += 1

    def test_method_args(self, count):
        self.method_count = count

    def test_method_string_arg(self, param):
        self.method_count += 1
        self.method_arg = param

    def test_method_kwargs(self, count=-1):
        self.method_count = count

    def test_redirect(self):
        return redirect("/something-here")

    def test_refresh_redirect(self):
        return LocationUpdate(redirect("/something-here"), title="new title")

    def test_hash_update(self):
        return HashUpdate("#test=1")

    def test_return_value(self):
        return "booya"

    def test_poll_update(self):
        return PollUpdate(timing=1000, disable=True, method="new_method")

    def test_validation_error(self):
        raise ValidationError({"check": "Check is required"}, code="required")

    def test_validation_error_no_code(self):
        raise ValidationError({"check": "Check is required"})

    def test_validation_error_string(self):
        raise ValidationError("Check is required", code="required")

    def test_validation_error_list(self):
        raise ValidationError(
            [ValidationError({"check": "Check is required"}, code="required")]
        )


class FakeModelComponent(UnicornView):
    template_name = "templates/test_component.html"
    flavors = Flavor.objects.all()

    def hydrate(self):
        self.flavors = Flavor.objects.all()


class FakeValidationForm(forms.Form):
    text = forms.CharField(min_length=3, max_length=10)
    date_time = forms.DateTimeField()
    number = forms.IntegerField()
    permanent = forms.BooleanField()


class FakeValidationComponent(UnicornView):
    template_name = "templates/test_component.html"
    form_class = FakeValidationForm

    text = "hello"
    number = ""
    date_time = datetime(2020, 9, 13, 17, 45, 14)
    permanent = True

    def set_text_no_validation(self):
        self.text = "no validation"

    def set_text_with_validation(self):
        self.text = "validation 33"
        self.validate()

    def set_number(self, number):
        self.number = number


class FakeComponentWithDictionary(UnicornView):
    template_name = "templates/test_component.html"
    dictionary: Dict = None

    def test_method(self):
        pass


class FakeComponentWithMessage(UnicornView):
    template_name = "templates/test_component_with_message.html"

    def test_message(self):
        assert self.request, "Expect a request in action methods"
        messages.success(self.request, "test success")

    def test_redirect_with_message(self):
        assert self.request, "Expect a request in action methods"
        messages.success(self.request, "test success")
        return redirect("/something-here")
