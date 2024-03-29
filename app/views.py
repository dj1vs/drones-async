from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import requests
import random
import concurrent.futures
import time

executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)

# Create your views here.

CALLBACK_URL = "http://127.0.0.1:80"

def get_allowed_hours(pk, token):
    time.sleep(5)
    return {
        "id": pk,
        "token": token,
        "allowed_hours": str(random.randint(7, 11)) + ':' + str(random.randint(18,21))
    }
    
def allowed_hours_callback(task):
    try:
        result = task.result()
    except concurrent.futures._base.CancelledError:
        return
    

    if (random.randint(1, 5) == 3):
        # return
        result["AllowedHours"] = "error"
    
    nurl = str(CALLBACK_URL + '/flight/set_allowed_hours?id=' + result["id"] + '&allowed_hours=' + result["allowed_hours"])
    headers = {"Content-Type": "application/json", "Authorization": "Bearer " + str(result["token"])}
    
    requests.put(nurl, json={}, timeout=3, headers=headers)


@api_view(['POST'])
def set_allowed_hours(request):
    print(request.data)
    if "token" not in request.data.keys():
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    if "token" in request.data.keys() and "pk" in request.data.keys():
        id = request.data["pk"]
        token = request.data["token"]
        task = executor.submit(get_allowed_hours, id, token)
        task.add_done_callback(allowed_hours_callback)
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)
