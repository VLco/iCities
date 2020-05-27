from django import forms
from .models import *


class ListFilter(forms.Form):
    class typeCities(forms.Form):
        all = forms.BooleanField(required=False, label="Все", label_suffix="")
        t1 = forms.BooleanField(required=False, label="Крупнейшие города с численностью населения от 1 млн. человек",
                                label_suffix="")
        t2 = forms.BooleanField(required=False,
                                label="Крупные города с численностью населения от 250 тыс. до 1 млн. человек",
                                label_suffix="")
        t3 = forms.BooleanField(required=False,
                                label="Большие города с численностью населения от 100 тыс. до 250 тыс. человек",
                                label_suffix="")
        t4 = forms.BooleanField(required=False,
                                label="Средние города с численностью населения от 50 тыс. до 100 тыс. человек",
                                label_suffix="")
        t5 = forms.BooleanField(required=False,
                                label="Малые города с численностью населения от 25 тыс. до 50 тыс. человек",
                                label_suffix="")
        t6 = forms.BooleanField(required=False,
                                label="Малые города с численностью населения от 5 тыс. до 25 тыс. человек",
                                label_suffix="")
        t7 = forms.BooleanField(required=False, label="Малые города с численностью населения до 5 тыс. человек",
                                label_suffix="")

    class climate(forms.Form):
        CLIMATE_CHOICES = [
            ('ALL', 'Все'),
            ('D', 'Дискомфортный'),
            ('C', 'Комфортный'),
        ]
        climate = forms.ChoiceField(choices=CLIMATE_CHOICES, label="Климат", widget=forms.RadioSelect)
