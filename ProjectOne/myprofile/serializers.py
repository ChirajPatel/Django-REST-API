from rest_framework import serializers

from myprofile.models import MyProfile


class MyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyProfile
        fields = "__all__"
