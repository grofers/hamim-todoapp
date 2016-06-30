import datetime
import hashlib

from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view
from rest_framework.decorators import authentication_classes
from rest_framework.decorators import permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ParseError

from .serializers import TaskSerializer, UserSerializer
from .models import Task


def hashed_password(old_pass):
    hash_object = hashlib.sha1(old_pass)
    hex_dig = hash_object.hexdigest()
    return hex_dig


@api_view(['GET', 'POST'])
def register(request, format=None):
    # GET method is used for testing. Remove later
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        responses = serializer.data
        return Response(responses)

    if request.method == 'POST':

        if ('username' not in request.data or
            'password' not in request.data or
            'first_name' not in request.data or
            'last_name' not in request.data):
                response = {}
                response['status'] = {'success': False,
                    'message': "Bad request"}
                return Response(response,
                    status=status.HTTP_400_BAD_REQUEST)

        try:
            new_pass = hashed_password(request.data['password'])
            auth_user = User(
                username = request.data['username'],
                password = new_pass,
                first_name = request.data['first_name'],
                last_name = request.data['last_name'],
            )
            auth_user.save()
            response = {}
            response['status'] = {'success': True,
                'message': "User created successfully"}
            return Response(response, status=status.HTTP_200_OK)

        except:
            response = {}
            response['status'] = {'success': False,
                'message': "Creation Failed. User already exists"}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def login(request, format=None):
    # GET method is used for testing. Remove later
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        responses = serializer.data
        return Response(responses)

    if request.method == 'POST':
        response = {}
        try:
            data = request.data
        except ParseError as error:
            response['status'] = {'success': False,
                'message': "Invalid JSON Format"}
            return Response(
                response,
                status=status.HTTP_400_BAD_REQUEST
            )

        if "username" not in data or "password" not in data:
            response['status'] = {'success': False,
                'message': "Required fields missing"}
            return Response(response,
                status=status.HTTP_400_BAD_REQUEST
            )

        new_pass = hashed_password(request.data['password'])
        user = User.objects.filter(username=request.data['username'],
            password=new_pass)
        if not user:
            response['status'] = {'success': False,
                    'message': "Incorrect username or password"}
            return Response(
                response,
                status=status.HTTP_404_NOT_FOUND
            )

        token = Token.objects.get_or_create(user=user[0])
        response['status'] = {'success': True, 'message': "Login success"}
        response['data'] = {'token': token[0].key}
        return Response(response, status=status.HTTP_200_OK)


@api_view(['POST', 'GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def tasks(request, format = None):
    if request.method == 'GET':

        query_days = request.GET.get('days', None)
        tasks = Task.objects.all().filter(owner=request.user).order_by('last_updated')

        if query_days is not None:
            query_days = int(query_days)
            start_date = datetime.date.today()
            end_date = start_date + timedelta(query_days + 1)
            tasks = Task.objects.all().filter(
                owner=request.user,
                scheduled_time__gte=start_date,
                scheduled_time__lte=end_date
            ).order_by('scheduled_time')

        response = {}
        serializer = TaskSerializer(tasks, many=True)

        tasks = serializer.data
        data = []
        totalCount = 0
        for task in tasks:
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
            user = request.user
            pending = True if 'pending' not in data else data['pending']
            scheduled_time = timezone.now() if 'scheduled_time' not in data else data['scheduled_time']
            task = Task(owner=user, description=data['description'],
                scheduled_time=scheduled_time, pending=pending)
            task.save()
            response['status'] = {'success': True,
                'message': "New Task Created"}
            return Response(response, status=status.HTTP_201_CREATED)
        except:
            response['status'] = {'success': False,
                'message': "Task Creation Failed"}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def modify_tasks(request, pk, format=None):
    response = {}
    if request.method == 'GET':
        tasks = Task.objects.filter(id=pk, owner=request.user)

        if not tasks:
            response['status'] = {'success': False, 'message': "Not Found"}
            return Response(response, status=status.HTTP_404_NOT_FOUND)

        serializer = TaskSerializer(tasks, many=True)
        tasks = serializer.data
        data = []
        for task in tasks:
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
            description = data['description']
            scheduled_time = data['scheduled_time']
            last_updated = timezone.now()
            data['last_updated'] = last_updated
            pending = data['pending']
            updated, created = Task.objects.update_or_create(
                id=id,
                owner=request.user,
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
            status=status.HTTP_200_OK)
        except:
            response['status'] = {'success': False,
                'message': "Update Failed"}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST)
