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
        input_text = serializer.validated_data.get("input_text")
        print(input_text)
        
        # Create a unique cache key based on the input text
        cache_key = f"search_api_{hashlib.md5(input_text.encode()).hexdigest()}"
        
        # Try to get cached response
        cached_result = cache.get(cache_key)
        if cached_result:
            response_serializer = SearchResponseSerializer({
                "output": cached_result
            })
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        
        # If not cached, make the actual API request
        output = requests.post(
            url=f"{URI}/classify-task", 
            headers=headers, 
            data=json.dumps({
                "user_id": str(self.request.user.id), 
                "task": input_text
            })
        ).json()
        
        # Cache the result for 36 hours (in seconds)
        cache.set(cache_key, output, 60 * 60 * 36)
        
        response_serializer = SearchResponseSerializer({
            "output": output
        })
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)