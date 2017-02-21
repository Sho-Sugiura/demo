import json

import requests
from django import forms
from django.conf import settings

DEFAULT_AMAZON_ML_ENDPOINT="https://realtime.machinelearning.us-east-1.amazonaws.com"

ANNUAL_INC_CHOICES = (
    (5000, "〜$10,000"),
    (17500, "$10,000〜25,000"),
    (37500, "$25,000〜50,000"),
    (75000, "$50,000〜100,000"),
    (125000, "$100,000〜150,000"),
    (175000, "$150,000〜200,000"),
    (425000, "$200,000〜650,000"),
    (2925000, "$650,000〜"),
)

INT_RATE_CHOICES = (
    (6.0, "7%/年未満"),
    (8.0, "7-9%/年以内"),
    (10.0, "9-11%/年以内"),
    (12.0, "11-13%/年以内"),
    (14.0, "13-15%/年以内"),
    (17.5, "15-20%/年以内"),
    (22.5, "20〜25%/年以内"),
    (28.0, "25%/年以上"),
)
BC_OPEN_TO_BUY_CHOICES = (
    (2500, "〜$2,500"),
    (3750, "$2,500〜5,000"),
    (7500, "$5,000〜10,000"),
    (12500, "$10,000〜15,000"),
    (17500, "$15,000〜20,000"),
    (25000, "$20,000〜30,000"),
    (165000, "$30,000〜300,000"),
    (850000, "$650,000〜"),
)

HOME_OWNERSHIP_CHOICES = (
    ("RENT", "賃貸"),
    ("OWN", "持ち家"),
    ("MORTGAGE", "持ち家(抵当)"),
    ("OTHER", "その他"),
)

class ExaminationForm(forms.Form):
    loan_amnt = forms.DecimalField(
        label="ご希望の融資額($)",
        min_value=0,
        max_value=100000,
        required=True,
        widget=forms.NumberInput()
    )
    int_rate = forms.ChoiceField(
        label="ご希望のローン金利",
        choices=INT_RATE_CHOICES,
        required=True,
        widget=forms.Select()
    )
    annual_inc = forms.ChoiceField(
        label="年収($)",
        choices=ANNUAL_INC_CHOICES,
        required=True,
        widget=forms.Select()
    )
    bc_open_to_buy = forms.ChoiceField(
        label="これまでのリボ払いの最大利用額",
        choices=BC_OPEN_TO_BUY_CHOICES,
        required=True,
        widget=forms.Select()
    )
    home_ownership = forms.ChoiceField(
        label="自宅の所有状況",
        choices=HOME_OWNERSHIP_CHOICES,
        required=True,
        widget=forms.Select()
    )

    def predict_loan_status(self):
        model_id = getattr(settings, "AMAZON_ML_MODEL_ID")
        amazon_ml_endpoint = getattr(settings, "AMAZON_ML_ENDPOINT", DEFAULT_AMAZON_ML_ENDPOINT)
        api_gateway_endpoint = getattr(settings, "API_GATEWAY_ENDPOINT")
        payload = {
            "MLModelId": model_id,
            "PredictEndpoint": amazon_ml_endpoint,
            "Record": {
                "loan_amnt": str(self.cleaned_data['loan_amnt']),
                "int_rate": str(self.cleaned_data['int_rate']),
                "grade": "3",
                "sub_grade": "33",
                "annual_inc": str(self.cleaned_data['annual_inc']),
                "verification_status": str(self.cleaned_data['annual_inc']),
                "bc_open_to_buy": str(self.cleaned_data['bc_open_to_buy']),
            }
        }
        response = requests.post(api_gateway_endpoint, data=json.dumps(payload))
        return response.json()
