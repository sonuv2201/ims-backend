from .models import HomeModel
from rest_framework import serializers


class HomeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeModel
        fields = "__all__"
