from django.shortcuts import render
from rest_framework import generics, permissions, mixins, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from .models import Post, Vote
from .serializers import PostSerializer, VoteSerializer


class PostList(generics.ListCreateAPIView, mixins.DestroyModelMixin):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        """ Custom method for saving user name and id"""
        serializer.save(poster=self.request.user)


class PostRetrieveDestory(generics.RetrieveDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def delete(self, request, *arg, **kwargs):
        """ Override delete function to make sure only users that 
        Posted the item in question can delete that specific post  """
        post = Post.objects.filter(pk=kwargs['pk'], poster=self.request.user)
        if post.exists():
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError('This isn\'t a post you created')


class VoteCreate(generics.CreateAPIView, mixins.DestroyModelMixin):
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """ Custom method for selecting data """
        user = self.request.user
        post = Post.objects.get(pk=self.kwargs['pk'])
        # voter == voter making request
        # post == post id
        return Vote.objects.filter(voter=user, post=post)

    def perform_create(self, serializer):
        """ Saving selected data """
        if self.get_queryset().exists():
            raise ValidationError('You have Voted, thank you')
        serializer.save(
            voter=self.request.user,
            post=Post.objects.get(pk=self.kwargs['pk'])
        )

    def delete(self, request, *args, **kwargs):
        """ Override delete function to make sure only users that 
        voted for the specific post can have delete functionality """
        if self.get_queryset().exists():
            self.get_queryset().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        else:
            raise ValidationError('You never voted for this post')
