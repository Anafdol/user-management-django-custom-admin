from people.models import Checkout
from rest_framework import serializers


class CheckoutSerializer(serializers.ModelSerializer):
    def validate(self, data):
        # check if checkin is active
        if not data['checkin'].active:
            raise serializers.ValidationError({'checkin': 'Checkin inválido.'})
        return data

    class Meta:
        model = Checkout
        fields = "__all__"
