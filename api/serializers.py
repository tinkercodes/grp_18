from rest_framework import serializers

from home.models import checkpost, vehicle_info, defaulter, closed_cases, staff

class CheckPostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = checkpost
        # fields = ('vrn', 'date', 'ruleCat_id', 'checkPost_id', 'time')
        fields = ('id','state', 'district', 'postCode')

# class DefaulterSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = checkPost
#         # fields = ('vrn', 'date', 'ruleCat_id', 'checkPost_id', 'time')
#         fields = ('state', 'district', 'postCode')

# class CheckPostSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = checkPost
#         # fields = ('vrn', 'date', 'ruleCat_id', 'checkPost_id', 'time')
#         fields = ('state', 'district', 'postCode')

class YourSerializer(serializers.Serializer):
   """Your data serializer, define your fields here."""
   comments = serializers.IntegerField()
   likes = serializers.IntegerField()

