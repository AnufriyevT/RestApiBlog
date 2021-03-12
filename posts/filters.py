from django_filters import FilterSet

from posts.models import Post


class PostFilter(FilterSet):
    class Meta:
        model = Post
        fields = {
            'pub_date': ['gte', 'lte'],
            'likes': ['gte', 'lte', 'exact'],
        }
