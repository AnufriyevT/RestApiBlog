from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

from posts.models import Post, User, Like, Favourite, Hashtags


class PostHashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtags
        fields = ("hashtag",)


class PostSerializer(serializers.ModelSerializer):
    hashtags = PostHashtagSerializer(many=True, )

    class Meta:
        model = Post
        fields = (
            'title',
            'text',
            'author',
            'pub_date',
            'likes',
            'hashtags',
        )

        extra_kwargs = {
            'author': {'read_only': True},
        }

    def create(self, validated_data):
        hashtags_data = validated_data.pop('hashtags')

        post = Post.objects.create(**validated_data)
        for hashtag in hashtags_data:
            tag = Hashtags.objects.create()
            tag.hashtag = hashtag.get("hashtag")
            tag.save()
            post.hashtags.add(tag)
        post.save()
        return post


class LikePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = (
            '__all__'
        )
        extra_kwargs = {
            'author': {'read_only': True},
            'post': {'read_only': True},
        }

    def update(self, instance: Post, validated_data):
        if not Like.objects.filter(post=instance, author=self.context['request'].user).exists():
            Like.objects.create(post=instance, author=self.context['request'].user)
            instance.likes += 1
            instance.save()
        return instance


class UnlikePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = (
            '__all__'
        )
        extra_kwargs = {
            'author': {'read_only': True},
            'post': {'read_only': True},
        }

    def update(self, instance: Post, validated_data):
        if Like.objects.filter(post=instance, author=self.context['request'].user).exists():
            Like.objects.filter(post=instance, author=self.context['request'].user).delete()
            instance.likes -= 1
            instance.save()
        return instance


class FavourPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourite
        fields = (
            '__all__'
        )
        extra_kwargs = {
            'author': {'read_only': True},
            'post': {'read_only': True},
        }

    def update(self, instance: Post, validated_data):
        Favourite.objects.get_or_create(post=instance, author=self.context['request'].user)
        return instance


class UnfavourPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourite
        fields = (
            '__all__'
        )
        extra_kwargs = {
            'author': {'read_only': True},
            'post': {'read_only': True},
        }

    def update(self, instance: Post, validated_data):
        Favourite.objects.filter(post=instance, author=self.context['request'].user).delete()
        return instance


class LikeSerializer(serializers.ModelSerializer):
    date = serializers.DateField(source="pub_date__date")
    likes_count = serializers.IntegerField()


class FavouriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourite
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
        )


class UserSerializerWithToken(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)

    def get_token(self, obj):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(obj)
        token = jwt_encode_handler(payload)

        return token

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)

        instance.save()

        return instance

    class Meta:
        model = User
        fields = ("token", "username", "first_name", "last_name", "password")
