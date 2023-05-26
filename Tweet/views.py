from django.shortcuts import render
from Tweet import utils

from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.

@api_view(['GET','POST'])
def home(request):

    if request.method == 'GET':
        daata = utils.all_tweets()
        return Response(daata)

    elif request.method == 'POST':
        daata = utils.insert_tweet(request.data)
        return Response(daata)

@api_view(['POST'])
def search(request):
    searchedData = utils.search(request.data)
    # print("searcheddata ",searchedData)
    return Response(searchedData)


