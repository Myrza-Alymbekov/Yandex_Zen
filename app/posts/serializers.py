from django.db import IntegrityError
from rest_framework import serializers

from .models import Post, Comment, Status


class PostSerializer(serializers.ModelSerializer):
    slug = serializers.ReadOnlyField(source='get_status')

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['author']


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['author', 'post']


class StatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Status
        fields = '__all__'
        read_only_fields = ['author', 'post']

    def create(self, validated_data):
        try:
            instance = super().create(validated_data)
        except IntegrityError:
            status = validated_data.pop('status')
            status_post = Status.objects.get(**validated_data)
            status_post.status = status
            status_post.save()
            instance = status_post
        return instance








