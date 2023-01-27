from rest_framework import serializers
from category.models import Category
from .models import Hotel, Like, Comment


    #краткая инфа --> http://localhost:8000/api/v1/posts/
class PostListSerializer(serializers.ModelSerializer):
    owner_username = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Hotel
        fields = ('id', 'owner', 'owner_username', 'title')

    def is_liked(self, post, user):
        return user.liked_posts.filter(post=post).exists()

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['likes_count'] = instance.likes.count()
        user = self.context['request'].user
        if user.is_authenticated:
            repr['is_liked'] = self.is_liked(instance, user)
        return repr


    #детальная инфа --> http://localhost:8000/api/v1/posts/<id>/
class PostDetailSerializer(serializers.ModelSerializer):
    owner_username = serializers.ReadOnlyField(source='owner.username')
    # category_name = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = Hotel
        fields = 'id', 'owner', 'owner_username', 'title', 'description', 'image', 'category', 'price', \
            'average_rating', 'stock', 'created_at'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['comments_count'] = instance.comments.count()
        rep['comments'] = CommentSerializer(instance.comments.all(),
                                            many=True).data
        # rep['images'] = PostImageSerializer(instance.images.all(),
        #                                     many=True).data
        rep['likes_count'] = instance.likes.count()
        rep['liked_users'] = LikeSerializer(instance=instance.likes.all(),
                                            many=True).data
        return rep


class PostCreateSerializer(serializers.ModelSerializer):
    # images = PostImageSerializer(many=True, read_only=False, required=False)

    class Meta:
        model = Hotel
        fields = 'id', 'owner', 'title', 'description', 'image', 'category', 'price', \
            'average_rating', 'stock', 'created_at'
        # fields = ('title', 'description', 'category', 'price')

    def create(self, validated_data):
        request = self.context.get('request')
        post = Hotel.objects.create(**validated_data)
        # images_data = request.FILES.getlist('images')
        # for image in images_data:
        #     PostImages.objects.create(image=image, post=post)
        return post


    #комменты --> http://localhost:8000/api/v1/comments/
class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')
    owner_username = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Comment
        fields = '__all__'


class UsersCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'body', 'post', 'created_at')

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['post_title'] = instance.post.title
        return repr


    #лайки --> http://localhost:8000/api/v1/posts/<id>/like/
class LikeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')
    owner_username = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Like
        fields = '__all__'

    def validate_data(self, attrs):
        request = self.context['request']
        user = request.user
        post = attrs['post']
        if post.likes.filter(owner=user).exists():
            raise serializers.ValidationError('You already liked post!')
        return attrs


class LikedPostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = 'post'

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['post_title'] = instance.post.title
        preview = instance.post.preview
        repr['post_preview'] = preview.url
        return repr
