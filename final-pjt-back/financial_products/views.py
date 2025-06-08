import requests, re
import numpy as np
import openai

from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import DepositProduct, SavingProduct, DepositOption, SavingOption
from .serializers import DepositSerializer, DepositOptionSerializer, DepositListSerializer, InterestDepositSerializer, DepositRecommendSerializer
from .serializers import SavingSerializer, SavingOptionSerializer, SavingListSerializer, InterestSavingSerializer, SavingRecommendSerializer
from accounts.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .questions import questions
from .analyze import classify_consumption
from .utils import generate_analysis_prompt, analyze_with_openai



# Create your views here.
API_KEY = settings.FIN_API_KEY

# < 초기 데이터 가져오기 >
@api_view(['GET'])
def get_deposit_products(request):
    deposit_API_URL = f'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json?auth={API_KEY}&topFinGrpNo=020000&pageNo=1'

    # JSON 데이터에서 'result'라는 키 값 가져와서, result 딕셔너리의 'baseList'라는 키 값 가져오기
    response = requests.get(deposit_API_URL)
    data = response.json().get('result', {})
    deposit_baselist = data.get('baseList', [])
    deposit_optionlist = data.get('optionList', [])

    # base는 한 개의 예금 상품 데이터
    for base in deposit_baselist:
        # 이미 같은 상품 코드가 DB에 있으면, 실행 안 하고 다음으로 넘어감 
        if DepositProduct.objects.filter(fin_prdt_cd=base.get('fin_prdt_cd')):
            continue
            
        deposit_product = {
            'dcls_month' : base.get('dcls_month'),
            'fin_prdt_cd': base.get('fin_prdt_cd'),
            'fin_co_no': base.get('fin_co_no'),
            'kor_co_nm': base.get('kor_co_nm'),
            'fin_prdt_nm': base.get('fin_prdt_nm'),
            'join_way': base.get('join_way'),
            'mtrt_int': base.get('mtrt_int'),
            'spcl_cnd': base.get('spcl_cnd'),
            'join_deny': base.get('join_deny'),
            'join_member': base.get('join_member'),
            'etc_note': base.get('etc_note'),
            'max_limit': base.get('max_limit')
        }
        print(f"Trying to save product: {deposit_product['fin_prdt_nm']}")
        serializer = DepositSerializer(data=deposit_product)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            print(f"Successfully saved product: {deposit_product['fin_prdt_nm']}")

    print("Finished processing products, now processing options...")

    for option in deposit_optionlist:
        prdt_cd = option.get('fin_prdt_cd')
        products = DepositProduct.objects.filter(fin_prdt_cd=prdt_cd)
        for product in products:
            deposit_option = {
                'deposit_product': product.id,
                'intr_rate_type': option.get('intr_rate_type'),
                'intr_rate_type_nm': option.get('intr_rate_type_nm'),
                'save_trm': option.get('save_trm'),
                'intr_rate': option.get('intr_rate'),
                'intr_rate2': option.get('intr_rate2'),
            }
            serializer = DepositOptionSerializer(data=deposit_option)
            if serializer.is_valid(raise_exception=True):
                serializer.save(deposit_product=product)
    return Response('Deposit 데이터 가져오기 성공')

@api_view(['GET'])
def get_saving_products(request):
    saving_API_URL = f'http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json?auth={API_KEY}&topFinGrpNo=020000&pageNo=1'
    saving_baselist = requests.get(saving_API_URL).json()['result']['baseList']
    saving_optionlist = requests.get(saving_API_URL).json()['result']['optionList']

    for base in saving_baselist:
        if SavingProduct.objects.filter(fin_prdt_cd=base.get('fin_prdt_cd')):
            continue
        saving_product = {
            'dcls_month' : base.get('dcls_month'),
            'fin_prdt_cd': base.get('fin_prdt_cd'),
            'fin_co_no': base.get('fin_co_no'),
            'kor_co_nm': base.get('kor_co_nm'),
            'fin_prdt_nm': base.get('fin_prdt_nm'),
            'join_way': base.get('join_way'),
            'mtrt_int': base.get('mtrt_int'),
            'spcl_cnd': base.get('spcl_cnd'),
            'join_deny': base.get('join_deny'),
            'join_member': base.get('join_member'),
            'etc_note': base.get('etc_note'),
            'max_limit': base.get('max_limit')
        }
        serializer = SavingSerializer(data=saving_product)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

    for option in saving_optionlist:
        prdt_cd = option.get('fin_prdt_cd')
        products = SavingProduct.objects.filter(fin_prdt_cd=prdt_cd)
        if option.get('rsrv_type') is None or option.get('rsrv_type_nm') is None:
            continue
        for product in products:
            saving_option = {
                'saving_product': product.id,
                'intr_rate_type': option.get('intr_rate_type'),
                'intr_rate_type_nm': option.get('intr_rate_type_nm'),
                'rsrv_type': option.get('rsrv_type'),
                'rsrv_type_nm': option.get('rsrv_type_nm'),
                'save_trm': option.get('save_trm'),
                'intr_rate': option.get('intr_rate'),
                'intr_rate2': option.get('intr_rate2'),  
            }
            serializer = SavingOptionSerializer(data=saving_option)
            if serializer.is_valid(raise_exception=True):
                serializer.save(saving_product=product)
    return Response('Saving 데이터 가져오기 성공')


# < 목록 조회 >
@api_view(['GET'])
def deposit_product_list(request):
    if request.method == 'GET':
        deposit_products = DepositProduct.objects.all()
        serializer = DepositListSerializer(deposit_products, many=True)
        
        # 로그인한 사용자의 경우 관심 상품 상태 추가
        if request.user.is_authenticated:
            data = serializer.data
            for product in data:
                product['is_interested'] = DepositProduct.objects.get(
                    fin_prdt_cd=product['fin_prdt_cd']
                ).interest_user.filter(id=request.user.id).exists()
            return Response(data)
        return Response(serializer.data)
    
@api_view(['GET'])
def saving_product_list(request):
    if request.method == 'GET':
        saving_products = SavingProduct.objects.all()
        serializer = SavingListSerializer(saving_products, many=True)
        
        # 로그인한 사용자의 경우 관심 상품 상태 추가
        if request.user.is_authenticated:
            data = serializer.data
            for product in data:
                product['is_interested'] = SavingProduct.objects.get(
                    fin_prdt_cd=product['fin_prdt_cd']
                ).interest_user.filter(id=request.user.id).exists()
            return Response(data)
        return Response(serializer.data)


# < 상세 정보 조회 >
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def deposit_detail(request, deposit_name):
    # 상품명과 예금 상품명이 같은 객체 찾기, 없으면 404 에러 발생
    deposit = get_object_or_404(DepositProduct, fin_prdt_nm=deposit_name)
    if request.method == 'GET':
        serializer = DepositListSerializer(deposit)
        return Response(serializer.data)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def saving_detail(request, saving_name):
    saving = get_object_or_404(SavingProduct, fin_prdt_nm=saving_name)
    if request.method == 'GET':
        serializer = SavingListSerializer(saving)
        return Response(serializer.data)
    

# # < 옵션 목록 조회 >
# # 옵션 리스트(여러 개, 모든 옵션 보기)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def deposit_option_list(request, deposit_name):
    deposit = get_object_or_404(DepositProduct, fin_prdt_nm=deposit_name)
    # 예금 상품명이 동일한 옵션 목록 조회
    deposit_options = DepositOption.objects.filter(deposit_product=deposit)

    if request.method == 'GET':
        serializer = DepositOptionSerializer(deposit_options, many=True)
        return Response(serializer.data)

# # 옵션 1개의 상세 정보(상품 코드, 옵션 ID로 조회)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def deposit_option_detail(request, deposit_code, option_id):
    deposit = get_object_or_404(DepositProduct, fin_prdt_cd=deposit_code)
    option = DepositOption.objects.get(deposit_product=deposit, id=option_id)
    if request.method == 'GET':
        serializer = DepositOptionSerializer(option)
        return Response(serializer.data)
    
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def saving_option_list(request, saving_name):
    saving = get_object_or_404(SavingProduct, fin_prdt_nm=saving_name)
    saving_options = SavingOption.objects.filter(saving_product=saving)

    if request.method == 'GET':
        serializer = SavingOptionSerializer(saving_options, many=True)
        return Response(serializer.data)

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def saving_option_detail(request, saving_code, option_id):
    saving = get_object_or_404(SavingProduct, fin_prdt_cd=saving_code)
    option = SavingOption.objects.get(saving_product=saving, id=option_id)
    if request.method == 'GET':
        serializer = SavingOptionSerializer(option)
        return Response(serializer.data)
    

# < 특정 은행의 예적금 조회 >

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def bank_deposit(request, bank_name):
    term = request.GET.get('term')  # 쿼리 파라미터로 기간 받기

    # 1. 은행 이름으로 기본 필터
    deposits = DepositProduct.objects.filter(kor_co_nm=bank_name)

    # 2. 기간 필터링
    # 전체 기간(쿼리파라미터 term이 없거나 빈문자열, '전체' 등) → 은행만 필터
    if not term or term == '전체':
        if deposits.exists():
            serializer = DepositListSerializer(deposits, many=True)
            return Response(serializer.data)
        else:
            return Response({'detail': '해당 은행의 상품이 없습니다.'}, status=status.HTTP_204_NO_CONTENT)
    else:
        # 기간(term)이 숫자라면 옵션까지 필터링
        try:
            term = int(term)
            # DepositOption 모델에서 save_trm(기간) 필터
            deposits = deposits.filter(depositoption__save_trm=term).distinct()
        except ValueError:
            return Response({'error': '기간은 숫자여야 합니다.'}, status=status.HTTP_400_BAD_REQUEST)

        if deposits.exists():
            serializer = DepositListSerializer(deposits, many=True)
            return Response(serializer.data)
        else:
            return Response({'detail': '해당 조건에 맞는 상품이 없습니다.'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def bank_saving(request, bank_name):
    term = request.GET.get('term')  # 쿼리 파라미터로 기간(개월) 받기

    # 1. 은행명으로 필터
    savings = SavingProduct.objects.filter(kor_co_nm=bank_name)

    # 2. 기간 필터링
    if not term or term == '전체':
        # 기간 미지정 또는 전체 → 은행 상품 전체 반환
        if savings.exists():
            serializer = SavingListSerializer(savings, many=True)
            return Response(serializer.data)
        else:
            return Response({'detail': '해당 은행의 적금 상품이 없습니다.'}, status=status.HTTP_204_NO_CONTENT)
    else:
        # 기간(term)이 숫자라면 옵션까지 필터링
        try:
            term = int(term)
            # SavingOption 모델의 save_trm(기간) 필터
            savings = savings.filter(savingoption__save_trm=term).distinct()
        except ValueError:
            return Response({'error': '기간은 숫자여야 합니다.'}, status=status.HTTP_400_BAD_REQUEST)

        if savings.exists():
            serializer = SavingListSerializer(savings, many=True)
            return Response(serializer.data)
        else:
            return Response({'detail': '해당 조건에 맞는 적금 상품이 없습니다.'}, status=status.HTTP_204_NO_CONTENT)


# < 기간에 맞는 상품 조회>
@api_view(['GET'])
def bank_deposit2(request, bank_name):
    if request.method == 'GET':
        # 1. 기간(save_trm) 파라미터 추출
        term = request.GET.get('term')
        
        # 2. 기본 쿼리셋: 해당 은행의 모든 예금 상품
        deposits = DepositProduct.objects.filter(kor_co_nm=bank_name)
        
        # 3. 기간 필터링 적용 (파라미터가 있을 경우)
        if term:
            try:
                term = int(term)  # 정수 변환 시도
                # 해당 기간 옵션이 있는 상품만 필터링 (중복 제거)
                deposits = deposits.filter(
                    depositoption__save_trm=term
                ).distinct()
            except ValueError:
                return Response(
                    {'error': '기간은 숫자로 입력해야 합니다.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # 4. 결과 반환
        if deposits.exists():
            serializer = DepositListSerializer(deposits, many=True)
            return Response(serializer.data)
        else:
            return Response(
                {'detail': '해당 조건에 맞는 상품이 없습니다.'},
                status=status.HTTP_204_NO_CONTENT
            )

# < 찜하거나 취소하는 기능 >
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_deposit(request, deposit_code):
    deposit = get_object_or_404(DepositProduct, fin_prdt_cd=deposit_code)
    user = request.user
    if deposit.interest_user.filter(id=user.id).exists(): # 이미 좋아요한 경우 좋아요 취소
        deposit.interest_user.remove(user)  
        return Response({'status': 'unliked'}, status=status.HTTP_200_OK)
    else:
        deposit.interest_user.add(user)  # 좋아요 추가
        return Response({'status': 'liked'}, status=status.HTTP_200_OK)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_saving(request, saving_code):
    saving = get_object_or_404(SavingProduct, fin_prdt_cd=saving_code)
    user = request.user
    if saving.interest_user.filter(id=user.id).exists():
        saving.interest_user.remove(user)  # 이미 좋아요한 경우 좋아요 취소
        return Response({'status': 'unliked'}, status=status.HTTP_200_OK)
    else:
        saving.interest_user.add(user)  # 좋아요 추가
        return Response({'status': 'liked'}, status=status.HTTP_200_OK)
    

# < 추천 >
def parse_monthly_limit(etc_note):
    if not etc_note:
        return None
    match = re.search(r'월\s*([\d,천만]+)만원', etc_note)
    if not match:
        return None
    s = match.group(1).replace(',', '').replace(' ', '')
    total = 0
    num = ''
    for ch in s:
        if ch.isdigit():
            num += ch
        elif ch == '천':
            total += int(num or '1') * 1000
            num = ''
        elif ch == '만':
            if num:
                total += int(num)
            total *= 10000
            num = ''
    if num:
        total += int(num)
    if '만' not in s:
        total *= 10000
    return total if total > 0 else None

@api_view(['GET'])
def deposit_recommend(request, username):
    user = get_object_or_404(User, username=username)
    salary = user.salary * 10000
    wealth = user.wealth * 10000
    desirePeriod = user.desirePeriod
    
    try:
        max_amount = int(request.GET.get('max_amount'))
    except (TypeError, ValueError):
        return Response({'error': 'max_amount 파라미터를 올바르게 입력하세요.'}, status=400)

    cnt_lst = [0] * 70 
    users = User.objects.all()
    for u in users:
        if (salary-10000000 <= u.salary <= salary+10000000) \
            and (wealth-1000000000 <= u.wealth <= wealth+1000000000) \
            and (desirePeriod-12 <= u.desirePeriod <= desirePeriod+12):
            for deposit in u.deposit.all():
                cnt_lst[int(deposit.id)] += 1

    cnt_tpl = [(cnt_lst[i], i) for i in range(len(cnt_lst))]
    cnt_tpl.sort(key=lambda x: -x[0])

    best = []
    for cnt, pid in cnt_tpl:
        if cnt == 0:
            continue
        try:
            product = DepositProduct.objects.get(id=pid)
        except DepositProduct.DoesNotExist:  
            continue
        limit = parse_monthly_limit(product.etc_note)
        if (limit is None) or (max_amount <= limit):
            best.append(pid)
        if len(best) == 5:
            break

    deposits = DepositProduct.objects.filter(id__in=best)
    serializer = DepositRecommendSerializer(deposits, many=True)
    return Response(serializer.data)

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def saving_recommend(request, username):
    user = get_object_or_404(User, username=username)
    salary = user.salary
    wealth = user.wealth
    desirePeriod = user.desirePeriod

    savings = user.saving.all()
    cnt_lst = [0] * 70
    
    users = User.objects.all()
    for user in users:
        if (salary-10000000 <= user.salary <= salary+10000000) \
            and (wealth-1000000000 <= user.wealth <= wealth+100000000) \
            and (desirePeriod-12 <= user.desirePeriod <= desirePeriod+12):
            savings = user.saving.all()
            for saving in savings:
                cnt_lst[int(saving.id)] += 1
    cnt_tpl = []
    for value in range(len(cnt_lst)):
        cnt_tpl.append((cnt_lst[value], value))
    cnt_tpl.sort(key= lambda x: -x[0])
    best = []
    for i in range(5):
        best.append(cnt_tpl[i][1])
    savings = SavingProduct.objects.filter(id__in=best)
    serializer = SavingRecommendSerializer(savings, many=True)
    return Response(serializer.data)

# < 관심 상품 목록 조회 >
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def interest_deposit_list(request):
    user = request.user
    deposits = user.interest_deposit.all()
    serializer = DepositListSerializer(deposits, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def interest_saving_list(request):
    user = request.user
    savings = user.interest_saving.all()
    serializer = SavingListSerializer(savings, many=True)
    return Response(serializer.data)

# < 예적금 추천 >

def get_top_similar_users(user, top_n=100):
    users = User.objects.exclude(id=user.id)
    salary_w = 1.0
    wealth_w = 1.0
    monthly_deposit_w = 1.0
    desire_period_w = 1.0

    user_vec = np.array([
        user.salary * salary_w,
        user.wealth * wealth_w,
        user.monthly_deposit * monthly_deposit_w,
        user.desire_period * desire_period_w
    ])
    scored = []
    for u in users:
        u_vec = np.array([
            u.salary * salary_w,
            u.wealth * wealth_w,
            u.monthly_deposit * monthly_deposit_w,
            u.desire_period * desire_period_w
        ])
        dist = np.linalg.norm(user_vec - u_vec)
        scored.append((dist, u.id))
    scored.sort()
    top_ids = [uid for _, uid in scored[:top_n]]
    return User.objects.filter(id__in=top_ids)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recommend_products(request):
    user = request.user
    similar_users = get_top_similar_users(user, top_n=100)

    recommended_saving = (
        SavingProduct.objects
        .filter(interest_user__in=similar_users)
        .annotate(join_count=Count('interest_user'))
        .order_by('-join_count')[:10]
    )
    recommended_deposit = (
        DepositProduct.objects
        .filter(interest_user__in=similar_users)
        .annotate(join_count=Count('interest_user'))
        .order_by('-join_count')[:10]
    )

    saving_data = SavingListSerializer(recommended_saving, many=True).data
    deposit_data = DepositListSerializer(recommended_deposit, many=True).data
    return Response({
        'saving_products': saving_data,
        'deposit_products': deposit_data,
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def calculate_saving_maturity(request):
    saving_name = request.data.get('saving_name')
    save_trm = int(request.data.get('save_trm'))
    monthly_amount = int(request.data.get('monthly_amount'))

    saving = get_object_or_404(SavingProduct, fin_prdt_nm=saving_name)
    options = SavingOption.objects.filter(saving_product=saving, save_trm=save_trm)
    if not options.exists():
        return Response({'error': '해당 기간의 옵션이 없습니다.'}, status=400)
    # 최대 우대금리 찾기
    max_option = options.order_by('-intr_rate2').first()
    max_rate = max_option.intr_rate2

    # 만기 수령액 계산 (단리, 세전)
    n = save_trm
    P = monthly_amount
    r = max_rate / 100
    maturity_amount = P * n + P * (n + 1) / 2 * n / 12 * r

    return Response({
        'saving_name': saving_name,
        'save_trm': n,
        'monthly_amount': P,
        'max_rate': max_rate,
        'maturity_amount': int(maturity_amount),
        'option_id': max_option.id,
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def calculate_deposit_maturity(request):
    deposit_name = request.data.get('deposit_name')
    save_trm = request.data.get('save_trm')
    amount = request.data.get('amount')

    if not deposit_name or not save_trm or not amount:
        return Response({'error': '필수 입력값이 누락되었습니다.'}, status=400)
    try:
        save_trm = int(save_trm)
        amount = int(amount)
    except ValueError:
        return Response({'error': '기간과 금액은 숫자여야 합니다.'}, status=400)

    deposit = get_object_or_404(DepositProduct, fin_prdt_nm=deposit_name)
    options = DepositOption.objects.filter(deposit_product=deposit, save_trm=save_trm)
    if not options.exists():
        return Response({'error': '해당 기간의 옵션이 없습니다.'}, status=400)
    # 최대 우대금리 찾기
    max_option = options.order_by('-intr_rate2').first()
    max_rate = max_option.intr_rate2

    # 만기 수령액 계산 (단리, 세전)
    n = save_trm
    P = amount
    r = max_rate / 100
    maturity_amount = P + (P * r * n / 12)

    return Response({
        'deposit_name': deposit_name,
        'save_trm': n,
        'amount': P,
        'max_rate': max_rate,
        'maturity_amount': int(maturity_amount),
        'option_id': max_option.id,
    })

@csrf_exempt
def consumption_test(request):
    if request.method == "GET":
        return JsonResponse({"questions": questions})
    elif request.method == "POST":
        data = json.loads(request.body)
        answers = data.get("answers", [])  # [0, 2, 1, ...]
        if len(answers) != 8:
            return JsonResponse({"error": "답변이 8개여야 합니다."}, status=400)
        # 선택지 텍스트로 변환
        answer_texts = [
            questions[i]["choices"][a] for i, a in enumerate(answers)
        ]
        result = classify_consumption(answers)
        prompt = generate_analysis_prompt(answer_texts)
        analysis = analyze_with_openai(prompt)
        return JsonResponse({
            "result": result,
            "analysis": analysis
        })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def ai_invest_advice(request):
    result_type = request.data.get('result_type')
    desc = request.data.get('desc')
    if not result_type:
        return Response({'error': '결과 타입이 필요합니다.'}, status=400)
    prompt = f"""당신은 금융 전문가입니다. 사용자의 소비 성향은 "{result_type}"입니다. ({desc})
이 소비 성향을 가진 사람에게 앞으로의 투자 전략이나 주의할 점을 짧은 2, 3문장으로 조언해줘. 말투는 완전 쌈뽕하고 유치한 느낌으로 가고 싶어."""

    openai.api_key = settings.OPENAI_API_KEY
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
        temperature=0.7,
    )
    advice = response.choices[0].message.content.strip()
    return Response({'advice': advice})