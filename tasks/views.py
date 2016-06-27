import datetime
import hashlib

from datetime import timedelta
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from .serializers import TaskSerializer, UserSerializer
from .models import Task, User


def hashed_password(old_pass):
    hash_object = hashlib.sha1(old_pass)
    hex_dig = hash_object.hexdigest()
    return hex_dig


@api_view(['POST', 'GET'])
def list_tasks(request, format = None):
    if request.method == 'GET':
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        data = JSONParser().parse(request)
        response = {}
        try:
            user = User.objects.get(id=data['user_id'])
            task = Task(user=user, description=data['description'],
                scheduled_time=data['scheduled_time'])
            task.save()
            response['status'] = {'success': True,
                'message': "Entry Added"}
            return Response(response, status=status.HTTP_201_CREATED)
        except:
            response['status'] = {'success': False,
                'message': "Entry not added"}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def modify_tasks(request, pk, format=None):
    u_id = User.objects.get(pk=pk)
    if request.method == 'GET':
        tasks = Task.objects.all().filter(user=u_id)
        serializer = ScheduleSerializer(schedule, many=True)
        try:
            return Response(serializer.data)
        except:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def list_users(request, format=None):
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        responses = serializer.data
        for response in responses:
            del response['password']
        return Response(responses)

    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                status=status.HTTP_201_CREATED)
        return Response(serializer.errors,
            status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
def modify_users(request, pk, format = None):
    try:
        user = User.objects.get(pk=pk)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        response = serializer.data
        del response['password']
        return Response(response)

    if request.method == 'PUT':
        data = JSONParser().parse(request)
        response = {}
        try:
            user_id = User.objects.get(id=data['id'])
            new_pass = hashed_password(data['password'])
            data['password'] = new_pass
            serializer = UserSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,
                    status=status.HTTP_201_CREATED)
        except:
            response['status'] = {'success': False,
                'message': "update failed"}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST)
