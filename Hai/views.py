# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.crypto import get_random_string
from .models import  AuthUserT, ContactUserT
from .serializers import UserPostSerializer,UserGetSerializer, UserSerializer,UserPutSerializer
from .serializers import UserRegisterSerializer,AuthUserTSerializer
import hashlib

class Register(APIView):
    """
    Register a new user.
    """
    def post(self, request, format=None):
        data = request.data
        password = data['password']
        email = data['email']
        data['token'] = self.getOrCreateToken()
        data['password'] = hashlib.md5(password.encode('utf-8')).hexdigest()
        serializer = UserRegisterSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            data.pop('password')
            data.pop('email')
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def getOrCreateToken(self):
        return get_random_string(length=6).upper()

class Token(APIView):
    """
    Register a new user.
    """
    def get(self, request, format=None):
        data = request.data
        data['email'] = request.GET['email']
        data['password'] = hashlib.md5(request.GET['password'].encode('utf-8')).hexdigest()
        serializer = AuthUserTSerializer(data=data)
        if serializer.is_valid():
            serializer.validate(data)
            data = serializer.data
            data.pop('password')
            data.pop('email')
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContactList(APIView):
    """
    List all contacts, or create a new user.
    """
    def get(self, request, format=None):
        token = request.META['HTTP_TOKEN']
        auth = AuthUserT.objects.filter(token=token).get()
        users = ContactUserT.objects.filter(authId=auth,is_valid=1)
        serializer = UserGetSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        token = request.META['HTTP_TOKEN']
        auth = AuthUserT.objects.filter(token=token).get()
        data = request.data
        data['authId'] = auth.authId
        serializer = UserPostSerializer(data=data,context={'authId':auth.authId})
        if serializer.is_valid():
            serializer.save()
            rep = serializer.data
            del (rep['authId'])
            return Response(rep, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = self.get_object(pk,request)
        user.is_valid = 0
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_object(self, pk, request):
        token = request.META['HTTP_TOKEN']
        try:
            auth = AuthUserT.objects.filter(token=token).get()
            return ContactUserT.objects.get(userId=pk, authId=auth,is_valid=1)
        except ContactUserT.DoesNotExist:
            raise Http404

class ContactDetail(APIView):
     """
     Retrieve, update or delete a user instance.
     """

     def get_object(self, pk,request):
         token = request.META['HTTP_TOKEN']
         try:
             auth = AuthUserT.objects.filter(token=token).get()
             return ContactUserT.objects.get(userId=pk, authId=auth,is_valid=1)
         except ContactUserT.DoesNotExist:
             raise Http404

     def get(self, request, pk, format=None):
         user = self.get_object(pk,request)
         user = UserSerializer(user)
         return Response(user.data)

     def put(self, request, pk, format=None):
         token = request.META['HTTP_TOKEN']
         user = self.get_object(pk, request)
         auth = AuthUserT.objects.filter(token=token).get()
         data = request.data
         data['authId'] = auth.authId
         serializer = UserPutSerializer(user,data=data)
         if serializer.is_valid():
             serializer.save()
             rep = serializer.data
             del (rep['authId'])
             return Response(rep, status=status.HTTP_201_CREATED)
         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

     def delete(self, request, pk, format=None):
         user = self.get_object(pk, request)
         user.is_valid = 0
         user.save()
         return Response(status=status.HTTP_204_NO_CONTENT)

     def get_object(self, pk, request):
         token = request.META['HTTP_TOKEN']
         try:
             auth = AuthUserT.objects.filter(token=token).get()
             return ContactUserT.objects.get(userId=pk, authId=auth,is_valid=1)
         except ContactUserT.DoesNotExist:
             raise Http404