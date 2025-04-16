from rest_framework.views import APIView
from rest_framework import permissions, status
from .serializers import SearchCreate,SearchResponseSerializer
from dotenv import load_dotenv
import os
import json
import requests
from rest_framework.response import Response
from django.core.cache import cache
import hashlib
load_dotenv()


URI= os.environ['ML_BACKEND_URI']
headers = {
  'Content-Type': 'application/json'
}


class SearchAPI(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer= SearchCreate(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data.get("input_text"))
        output= requests.post(url= f"{URI}/classify-task", headers=headers, data= json.dumps({"user_id": str(self.request.user.id), "task": serializer.validated_data.get("input_text")})).json()
        response_serializer= SearchResponseSerializer({
            "output": output
        })
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)