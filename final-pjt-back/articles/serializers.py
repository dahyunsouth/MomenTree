from rest_framework import serializers
from .models import Article, Comment


# 전체 게시글 직렬화
class ArticleListSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField(source='user.nickname', read_only=True)
    profile_image = serializers.ImageField(source='user.profile_image', read_only=True)
    class Meta:
        model = Article
        fields = (
            'id',
            'title',
            'content',
            'nickname',
            'profile_image',
            'created_at',
        )
        read_only_fields = ('nickname', 'profile_image', 'created_at', 'id')
        

# 단일 게시글 직렬화
class ArticleSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField(source='user.nickname', read_only=True)
    profile_image = serializers.ImageField(source='user.profile_image', read_only=True)
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    # 게시글하나(1) : 댓글들(N)
    class CommentDetailSerializer(serializers.ModelSerializer):
        nickname = serializers.CharField(source='user.nickname', read_only=True)
        profile_image = serializers.ImageField(source='user.profile_image', read_only=True)
        user_id = serializers.IntegerField(source='user.id', read_only=True)
        class Meta:
            model = Comment
            fields = (
                'id',
                'content',
                'nickname',
                'profile_image',
                'user_id',
            )
    user_name = serializers.CharField(source='user.username', read_only=True)
    comment_set = CommentDetailSerializer(many=True, read_only=True)
    # comment_set : 역참조, count : 메서드
    comment_count = serializers.IntegerField(
        source = 'comment_set.count', read_only = True
    )
    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ('user', 'nickname', 'profile_image', 'created_at', 'id')
        

class CommentSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField(source='user.nickname', read_only=True)
    profile_image = serializers.ImageField(source='user.profile_image', read_only=True)
    # 1. 댓글을 조회했을때 게시글의 제목도 같이 나오게
    class ArticleTitleSerializer(serializers.ModelSerializer):
        class Meta:
            model = Article
            fields = ('title', )
    # 댓글 조회했을 때 같이 응답받는 게시글의 제목은 읽기 전용
    article = ArticleTitleSerializer(read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('user', 'nickname', 'profile_image', 'article')
