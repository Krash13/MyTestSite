from rest_framework import serializers
from .models import Task,Comment,File



class TaskSerializer(serializers.Serializer):
    name=serializers.CharField(max_length=120)
    body=serializers.CharField()
    customer_id=serializers.IntegerField(required=False)
    executor_id = serializers.IntegerField(required=False)
    created = serializers.DateTimeField(required=False)
    completed=serializers.DateTimeField(required=False)
    def create(self, validated_data):
        return Task.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.body = validated_data.get('body', instance.body)
        instance.executor_id = validated_data.get('executor_id', instance.executor_id)
        instance.save()
        return instance

class CommentSerializer(serializers.Serializer):
    task_id=serializers.IntegerField()
    text=serializers.CharField()
    author_id=serializers.IntegerField(required=False)
    answer=serializers.CharField(required=False)
    created = serializers.DateTimeField(required=False)

    def create(self, validated_data):
        return Comment.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.text = validated_data.get('text', instance.text)
        instance.save()
        return instance

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = "__all__"