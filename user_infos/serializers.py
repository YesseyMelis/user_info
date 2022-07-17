from rest_framework import serializers

from user_infos.models import UserInfo


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = (
            'id',
            'email',
            'telegram',
            'instagram',
            'phone'
        )
