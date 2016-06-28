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
        query_days = request.GET.get('days', None)
        tasks = Task.objects.all().order_by('last_updated')

        if query_days is not None:
            query_days = int(query_days)
            start_date = datetime.date.today()
            end_date = start_date + timedelta(query_days + 1)
            tasks = Task.objects.filter(
                scheduled_time__gte=start_date,
                scheduled_time__lte=end_date
            ).order_by('scheduled_time')

        response = {}
        serializer = TaskSerializer(tasks, many=True)
        tasks = serializer.data
        data = []
        totalCount = 0
        for task in tasks:
            del task['user']
            data.append(task)
            totalCount += 1

        try:
            response['data'] = {'tasks': data}
            response['status'] = {'success': True}
            response['_metadata'] = {'totalCount': totalCount,
                'days': (0 if query_days is None else query_days)}
            return Response(response,
                status=status.HTTP_200_OK)
        except:
            response['status'] = {'success': False}
            return Response(response,
                status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'POST':
        data = JSONParser().parse(request)
        response = {}
        try:
            user = User.objects.get(id=data['user_id'])
            pending = True if 'pending' not in data else data['pending']
            task = Task(user=user, description=data['description'],
                scheduled_time=data['scheduled_time'], pending=pending)
            task.save()
            response['status'] = {'success': True,
                'message': "New Task Created"}
            return Response(response, status=status.HTTP_201_CREATED)
        except:
            response['status'] = {'success': False,
                'message': "Task Creation Failed"}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
def modify_tasks(request, pk, format=None):
    u_id = User.objects.get(pk=pk)
    response = {}
    if request.method == 'GET':
        tasks = Task.objects.filter(id=pk)
        serializer = TaskSerializer(tasks, many=True)
        tasks = serializer.data
        data = []
        for task in tasks:
            del task['user']
            data.append(task)

        try:
            response['data'] = {'tasks': data}
            response['status'] = {'success': True}
            return Response(response,
                status=status.HTTP_200_OK)
        except:
            response['status'] = {'success': False}
            return Response(response,
                status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'PUT':
        data = JSONParser().parse(request)
        response = {}
        try:
            id = pk
            user = User.objects.get(id=data['user_id'])
            description = data['description']
            scheduled_time = data['scheduled_time']
            last_updated = datetime.datetime.now()
            data['last_updated'] = last_updated
            pending = data['pending']
            updated, created = Task.objects.update_or_create(
                id=id,
                user=user,
                description=description,
                scheduled_time=scheduled_time,
                last_updated=last_updated,
                pending=pending,
                defaults=data
                )
            updated.save()
            response['status'] = {'success': True,
                'message': "Update Successful"}
            return Response(response,
            status=status.HTTP_201_CREATED)
        except:
            response['status'] = {'success': False,
                'message': "Update Failed"}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST)



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
        data = JSONParser().parse(request)
        response = {}
        try:
            new_pass = hashed_password(data['password'])
            data['password'] = new_pass
            serializer = UserSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                response['status'] = {'success': True,
                    'message': "Created Successfully"}
                return Response(response,
                    status=status.HTTP_201_CREATED)
        except:
            response['status'] = {'success': False,
                'message': "Creation Failed"}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

