from rest_framework.views import APIView
from rest_framework import permissions
from serializers import SearchCreate,SearchResponseSerializer
from dotenv
import requests
# Create your views here.
class SearchAPI(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer= SearchCreate(data=request.data)
        serializer.save(raise_exception=True)


        response_serializer= SearchResponseSerializer({
            'output': 
        })