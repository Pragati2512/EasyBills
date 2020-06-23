from rest_framework import serializers
from Profile.models import Profile,User
from docdata.models import RawData, ProcessedData, GroupDataLink

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']


class RawDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawData
        fields = '__all__'

class ProcessedDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessedData
        fields = '__all__'

class GroupDataLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupDataLink
        fields = '__all__'

