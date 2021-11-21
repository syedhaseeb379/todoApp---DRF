from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from .serializers import TaskSerializer

import datetime

from .models import Task
# Create your views here.

@api_view(['GET'])
def apiOverview(request):
	api_urls = {
		'List':'/task-list/',
		'Detail View':'/task-detail/<str:pk>/',
		'Create':'/task-create/',
		'Update':'/task-update/<str:pk>/',
		'Delete':'/task-delete/<str:pk>/',
		}

	return Response(api_urls)

@api_view(['GET'])
def taskList(request):
	tasks = Task.objects.all().order_by('-id')
	serializer = TaskSerializer(tasks, many=True)
	return Response(serializer.data)

@api_view(['GET'])
def taskDetail(request, pk):
	tasks = Task.objects.get(id=pk)
	serializer = TaskSerializer(tasks, many=False)
	return Response(serializer.data)


@api_view(['POST'])
def taskCreate(request):
	serializer = TaskSerializer(data=request.data)

	if serializer.is_valid():
		serializer.save()

	return Response(serializer.data)

@api_view(['POST'])
def taskUpdate(request, pk):
	task = Task.objects.get(id=pk)
	serializer = TaskSerializer(instance=task, data=request.data)

	if serializer.is_valid():
		serializer.save()

	return Response(serializer.data)


@api_view(['DELETE'])
def taskDelete(request, pk):
	task = Task.objects.get(id=pk)
	task.delete()

	return Response('Item succsesfully delete!')



"""

1. Write a GET API which receives current_time as query parameter which is read and set as cookie
2. Write a POST API which receives ‘itemname’ and ‘timestring’ in post data and current_time from cookies now call the IsItemAvailable 
function with these there arguments and return the response"""




def ifAvailable(currentTime, itemName, timeString):
    timeranges = timeString.split(',')
#     currentTime = datetime.datetime.now().strftime("%H:%M")
    currentTime = datetime.datetime.strptime(currentTime, '%H:%M').time()
    # currentTime = datetime.datetime.now().time()
    flag = False
    for i in timeranges:
        timeLimits = i.split('-')
        lowTimeLimit = datetime.time(int(timeLimits[0][:2]), int(timeLimits[0][3:]))
        highTimeLimit = datetime.time(int(timeLimits[1][:2]), int(timeLimits[1][3:]))
        if currentTime > lowTimeLimit and currentTime < highTimeLimit:
            flag = True
    
    return flag

@api_view(['GET'])
def getTime(request, current_time):
	if request.method == 'GET':
		value = request.COOKIES.get('cookie')
		if value != None:
			print(value)
			return Response('WORKS')
		else:
			response = Response('Setting a cookie')
			response.set_cookie('cookie', current_time)
			return Response("Time saved")
		

@api_view(['POST'])
def postAvailableData(request):
	data = request.data
	currentTime = request.COOKIES.get('cookie')
	flag = ifAvailable(currentTime, data["itemName"], data["timeString"])
	currentTime = datetime.datetime.now().time()
	displayTime = currentTime.strftime("%H:%M")
	if flag == True:
		return Response(f"{data['itemName']} available if current time is {displayTime}")
	else:
		return Response(f"{data['itemName']} not available")


