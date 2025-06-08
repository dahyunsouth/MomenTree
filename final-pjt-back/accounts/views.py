import urllib.parse
import requests 
from .models import User
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.shortcuts import redirect
from django.templatetags.static import static
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import SignupSerializer


@api_view(['POST'])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        user = serializer.save()
        image_url = user.profile_image.url if user.profile_image else static('default.jpg')
        return Response(
            {
                'message': '회원가입이 완료되었습니다.',
                'user': {
                    'username': user.username,
                    'nickname': user.nickname,
                    'email': user.email,
                    'age': user.age,
                    'profile_image': request.build_absolute_uri(image_url)
                }
            }, 
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    username = request.data.get('id')  # 프론트엔드에서 보내는 'id' 필드 사용
    password = request.data.get('password')
    
    if username is None or password is None:
        return Response({'error': '아이디와 비밀번호를 모두 입력하세요.'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = authenticate(username=username, password=password)
    
    if not user:
        return Response({'error': '아이디 또는 비밀번호가 잘못되었습니다.'}, status=status.HTTP_401_UNAUTHORIZED)
    
    token, _ = Token.objects.get_or_create(user=user)
    
    return Response({
        'token': token.key,
        'user': {
            'username': user.username,
            'nickname': user.nickname,
            'email': user.email,
            'age': user.age
        }
    })

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout(request):
    # 현재 사용자의 토큰을 삭제
    request.user.auth_token.delete()
    return Response({'message': '로그아웃되었습니다.'})

@api_view(['GET', 'PUT', 'PATCH'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def profile(request):
    user = request.user
    if request.method in ['PUT', 'PATCH']:
        data = request.data.copy()
        # username(아이디) 수정 불가
        data.pop('username', None)
        data.pop('id', None)
        serializer = SignupSerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            image_url = user.profile_image.url if user.profile_image and hasattr(user.profile_image, 'url') else static('default.jpg')
            return Response({
                'message': '프로필이 수정되었습니다.',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'nickname': user.nickname,
                    'email': user.email,
                    'age': user.age,
                    'salary': user.salary,
                    'wealth': user.wealth,
                    'monthly_deposit': user.monthly_deposit,
                    'desire_period': user.desire_period,
                    'profile_image': request.build_absolute_uri(image_url)
                }
            })
        return Response(serializer.errors, status=400)
    image_url = user.profile_image.url if user.profile_image and hasattr(user.profile_image, 'url') else static('default.jpg')
    return Response({
        'user': {
            'id': user.id,
            'username': user.username,
            'nickname': user.nickname,
            'email': user.email,
            'age': user.age,
            'salary': user.salary,
            'wealth': user.wealth,
            'monthly_deposit': user.monthly_deposit,
            'desire_period': user.desire_period,
            'profile_image': request.build_absolute_uri(image_url)
        }
    }) 

# 소셜 로그인 (구글)
# def google_login(request):
#     client_id    = settings.GOOGLE_CLIENT_ID
#     redirect_uri = request.build_absolute_uri('/accounts/google/callback/')
#     params = {
#         "client_id":     client_id,
#         "redirect_uri":  redirect_uri,
#         "response_type": "code",
#         "scope":         "openid email profile",
#         "prompt":        "select_account",
#     }
#     auth_url = "https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode(params)
#     return redirect(auth_url)

# def google_callback(request):
#     code = request.GET.get("code")
#     if not code:
#         return redirect('boards:index')

#     # 1) 토큰 요청
#     token_url = "https://oauth2.googleapis.com/token"
#     data = {
#         "code":          code,
#         "client_id":     settings.GOOGLE_CLIENT_ID,
#         "client_secret": settings.GOOGLE_CLIENT_SECRET,
#         "redirect_uri":  request.build_absolute_uri('/accounts/google/callback/'),
#         "grant_type":    "authorization_code",
#     }
#     token_res    = requests.post(token_url, data=data).json()
#     access_token = token_res.get("access_token")
#     if not access_token:
#         return redirect('boards:index')

#     # 2) 사용자 정보 요청
#     userinfo_url = "https://www.googleapis.com/oauth2/v3/userinfo"
#     headers      = {"Authorization": f"Bearer {access_token}"}
#     info         = requests.get(userinfo_url, headers=headers).json()
#     email        = info.get("email")
#     name         = info.get("name")
#     if not email:
#         return redirect('boards:index')

#     # 3) 사용자 생성 또는 조회
#     user, created = User.objects.get_or_create(
#         username=email,
#         defaults={"first_name": name}
#     )
#     # 4) 로그인
#     auth_login(request, user)
#     return redirect('boards:index')
