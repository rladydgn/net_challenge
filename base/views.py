from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from base.serializers import UserDataSerializer
from base.tmap import get_road_info_api


class LocationAPIVIew(APIView):
    def get(self, request):
        # query string에 필요한 정보가 없을 경우
        if 'lat' not in request.GET:
            return Response("lat bad", status=status.HTTP_400_BAD_REQUEST)
        if 'lon' not in request.GET:
            return Response("lon bad", status=status.HTTP_400_BAD_REQUEST)
        if 'limit' not in request.GET:
            return Response("limit bad", status=status.HTTP_400_BAD_REQUEST)
        if request.GET['limit'] not in ["0", "1"]:
            return Response("bad", status=status.HTTP_400_BAD_REQUEST)

        # tmap api 호출하여 위도, 경도에 가장 가까운 도로에 대한 정보(dict)
        res = get_road_info_api(request.GET['lon'], request.GET['lat'])

        # serialize 데이터
        data = {
            "user_id": "temp2",
            "limit_speed": res['resultData']['header']['speed'],
            "road_name": res['resultData']['header']['roadName'],
            'longitude': request.GET['lon'],
            'latitude': request.GET['lat'],
            'do_limit': request.GET['limit']
        }

        serializer = UserDataSerializer(data=data)

        # 데이터가 유효한지 확인한다.
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response("bad", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
