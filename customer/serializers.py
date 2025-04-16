from rest_framework import serializers

class SearchCreate(serializers.Serializer):
    input_text= serializers.CharField(max_length=500)
    class Meta:
        fields= ['input_text']

class SearchResponseSerializer(serializers.Serializer):
    output = serializers.JSONField()

    class Meta:
        fields= ['output']