from rest_framework import serializers
from .models import Status, Tran

class Stsz(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = "__all__"


class Transz(serializers.ModelSerializer):
    class Meta:
        model = Tran
        fields = "__all__"

