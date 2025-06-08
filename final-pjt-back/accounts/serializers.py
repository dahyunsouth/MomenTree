from rest_framework import serializers
from .models import User
from django.db import IntegrityError

class SignupSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='username')
    monthlyDeposit = serializers.CharField(required=True)
    desirePeriod = serializers.CharField(required=True)
    age = serializers.CharField(required=True)
    salary = serializers.CharField(required=True)
    wealth = serializers.CharField(required=True)
    deposit = serializers.JSONField(required=False, allow_null=True)
    saving = serializers.JSONField(required=False, allow_null=True)
    name = serializers.CharField(required=False, allow_blank=True)
    profile_image = serializers.ImageField(required=False, allow_null=True)
    
    class Meta:
        model = User
        fields = ('id', 'password', 'nickname', 'email', 'age', 'monthlyDeposit', 'desirePeriod', 'salary', 'wealth', 'deposit', 'saving', 'name', 'profile_image')
        extra_kwargs = {
            'password': {'write_only': True},
        }
    
    def validate(self, data):
        print("Received data in validate:", data)  # 디버깅용 로그
        try:
            # source 필드 처리
            monthly_deposit = int(data.pop('monthlyDeposit'))
            desire_period = int(data.pop('desirePeriod'))
            
            # 나머지 필드 처리
            data['monthly_deposit'] = monthly_deposit
            data['desire_period'] = desire_period
            data['age'] = int(data['age'])
            data['salary'] = int(data['salary'])
            data['wealth'] = int(data['wealth'])
            
            # username 필드 처리
            if 'username' not in data and 'id' in data:
                data['username'] = data.pop('id')
            
            return data
        except (ValueError, TypeError, KeyError) as e:
            print(f"Error during validation: {str(e)}")  # 디버깅용 로그
            raise serializers.ValidationError({'error': f'데이터 형식이 올바르지 않습니다: {str(e)}'})
    
    def create(self, validated_data):
        print("Data in create:", validated_data)  # 디버깅용 로그
        
        # 불필요한 필드 제거
        validated_data.pop('deposit', None)
        validated_data.pop('saving', None)
        validated_data.pop('name', None)
        profile_image = validated_data.pop('profile_image', None)
        try:
            user = User.objects.create_user(
                username=validated_data['username'],
                password=validated_data['password'],
                nickname=validated_data['nickname'],
                email=validated_data['email'],
                age=validated_data['age'],
                monthly_deposit=validated_data['monthly_deposit'],
                desire_period=validated_data['desire_period'],
                salary=validated_data['salary'],
                wealth=validated_data['wealth']
            )
            if profile_image:
                user.profile_image = profile_image
            else:
                user.profile_image = 'default.jpg'
            user.save()
            return user
        except IntegrityError:
            raise serializers.ValidationError({'error': '이미 사용 중인 아이디입니다. 다른 아이디를 선택해주세요.'})
        except Exception as e:
            print(f"Error during user creation: {str(e)}")  # 디버깅용 로그
            raise serializers.ValidationError({'error': f'사용자 생성 중 오류가 발생했습니다: {str(e)}'})
    
    def update(self, instance, validated_data):
        # username은 수정 불가
        validated_data.pop('username', None)
        validated_data.pop('id', None)
        for attr, value in validated_data.items():
            if attr == 'profile_image' and value:
                instance.profile_image = value
            elif hasattr(instance, attr):
                setattr(instance, attr, value)
        instance.save()
        return instance 