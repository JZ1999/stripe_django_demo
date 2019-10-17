import stripe
from rest_framework import serializers


class DemoChargeSerializer(serializers.Serializer):
    def create(self, validated_data, *args, **kwargs):
        token = stripe.Token.create(
            card={
                'number': validated_data["cc"],
                'exp_month': validated_data["expiration_month"],
                'exp_year': validated_data["expiration_year"],
                'cvc': validated_data["cvv"],
            },
        )

        charge = stripe.Charge.create(
            amount=400,
            currency='usd',
            description='DRF test payment',
            source=token
        )

        return charge

    # NOTA este regex es solo para Visa, MasterCard, American Express, Diners Club, Discover, y JCB
    cc_regex = r'^(?:4[0-9]{12}(?:[0-9]{3})?|[25][1-7][0-9]{14}|6(?:011|5[0-9][0-9])[0-9]{12}|3[47][0-9]{13}|3(?:0[0-5]|[68][0-9])[0-9]{11}|(?:2131|1800|35\d{3})\d{11})$'
    cc = serializers.RegexField(regex=cc_regex)

    cvv_regex = r'^[0-9]{3,4}$'
    cvv = serializers.RegexField(regex=cvv_regex)

    expiration_month_regex = r'^(0?[1-9]|1[012])$'
    expiration_month = serializers.RegexField(regex=expiration_month_regex)

    expiration_year_regex = r'^[0-9]{4}$'
    expiration_year = serializers.RegexField(regex=expiration_year_regex)
