from rest_framework import serializers
from ApiArriendosAlegria.models import Usuario


class SerializadorTokenUsuario(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('username', 'email')


class SerializadorUsuario(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'

    def create(self, validated_data):
        user = Usuario(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        updated_user = super().update(instance, validated_data)
        updated_user.set_password(validated_data['password'])
        updated_user.save()
        return updated_user


class SerializadorListaUsuario(serializers.ModelSerializer):
    class Meta:
        model = Usuario

    def to_representation(self, instance):
        return {
            'id': instance['id'],
            'username': instance['username'],
            'email': instance['email'],
            'password': instance['password'],
        }