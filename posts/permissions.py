from rest_framework.permissions import BasePermission

from posts.models import Post


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        try:
            user_profile = Post.objects.get(
                pk=view.kwargs['pk'])
        except (Post.DoesNotExist, Post.MultipleObjectsReturned):
            return False

        if request.user.profile == user_profile:
            return True
        return False
