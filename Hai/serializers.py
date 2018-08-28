from .models import ContactUserT, AuthUserT
from rest_framework import serializers
from django.db import models
import json


class UserRegisterSerializer(serializers.ModelSerializer):
    def validate_email(self, value):
        if AuthUserT.objects.filter(email=value).exists():
            raise serializers.ValidationError('already exists')
        return value
    class Meta:
        model = AuthUserT
        fields = ('email','password', 'token')


class AuthUserTSerializer(serializers.ModelSerializer):
    def validate_email(self, value):
        if AuthUserT.objects.filter(email=value).exists():
           pass
        else:
            raise serializers.ValidationError('Email id doesnot exist')
        return value

    def validate_password(self, value):
        data = self.get_initial()
        email = data.get('email')
        if AuthUserT.objects.filter(email=email,password=value).exists():
           pass
        else:
            raise serializers.ValidationError('password doesnot match')
        return value

    def validate(self, data):
        authUser = AuthUserT.objects.filter(password=data.get('password'),email=data.get('email')).get()
        data['token'] = authUser.token
        return authUser

    class Meta:
        model = AuthUserT
        fields = ('email','password','token')



class UserGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUserT
        #fields = ('userId','firstName', 'lastName', 'phone','adress','userEmail','authId')
        exclude = ('authId',)

class UserSerializer (serializers.ModelSerializer):
    class Meta:
         model = ContactUserT
         fields = ( 'firstName', 'lastName', 'phone', 'userEmail','adress','userId')

class UserPostSerializer(serializers.ModelSerializer):
    authId = AuthUserT()
    userId = models.IntegerField()
    class Meta:
        model = ContactUserT
        fields = ( 'firstName', 'lastName', 'phone', 'userEmail','adress','authId','userId')
    def create(self, validated_data):
        haiUser = ContactUserT.objects.create(**validated_data)
        return haiUser

class UserPutSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUserT
        fields = ( 'firstName', 'lastName', 'phone', 'userEmail','adress','userId','authId')
    def update(self, instance, validated_data):
        instance.firstName = validated_data.get('firstName', instance.firstName)
        instance.lastName = validated_data.get('lastName', instance.lastName)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.userEmail = validated_data.get('userEmail', instance.userEmail)
        instance.adress = validated_data.get('adress', instance.adress)
        instance.userId = validated_data.get('userId', instance.userId)
        instance.authId = validated_data.get('authId', instance.authId)
        instance.save()
        return instance


'''

class UserPostSerializer_v2(serializers.ModelSerializer):
    authId = AuthUserT()
    userId = models.IntegerField()
    print (UserSerializer())
    class Meta:
        model = ContactUserT
        fields = ( 'firstName', 'lastName', 'phone', 'userEmail','adress','authId', 'userId')
    def create(self, validated_data):
        haiUser = ContactUserT.objects.create(**validated_data)
        haiUser.save()
        i = UserSerializer(haiUser)
        print(i.data)
        return UserSerializer(haiUser).data

class UserPostSerializer_v1(serializers.ModelSerializer):
    authId = AuthUserT()
    class Meta:
         model = ContactUserT
         fields = ( 'firstName', 'lastName', 'phone', 'userEmail','adress','authId')
    def create(self, validated_data):
        haiUser = ContactUserT.objects.create(**validated_data)
        haiUser.save()
        return UserSerializer ( haiUser )


'''
