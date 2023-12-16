from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import requests
import random

# Create your views here.

CALLBACK_URL = "http://0.0.0.0:8000/stocks"

def get_random_status():
    return bool(random.getrandbits(1))

def send_status(pk, status):
    nurl = str(CALLBACK_URL + str(pk) + '/put/')
    answer = {"is_growing": status}
    requests.put(nurl, data=answer, timeout=3)

@api_view(['POST'])
def set_status(request):
    if "pk" in request.data.keys():
        id = request.data["pk"]
        stat = get_random_status()
        send_status(id, stat)
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)
