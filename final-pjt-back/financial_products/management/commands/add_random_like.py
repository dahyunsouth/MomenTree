from django.core.management.base import BaseCommand
import random
from accounts.models import User
from financial_products.models import DepositProduct, SavingProduct

class Command(BaseCommand):
    help = '유저들에게 임의로 상품 찜(M2M) 관계를 생성합니다.'

    def handle(self, *args, **options):
        users = User.objects.all()
        saving_products = list(SavingProduct.objects.all())
        deposit_products = list(DepositProduct.objects.all())

        for user in users:
            random_savings = random.sample(saving_products, k=min(len(saving_products), random.randint(2, 5)))
            for saving in random_savings:
                saving.interest_user.add(user)

            random_deposits = random.sample(deposit_products, k=min(len(deposit_products), random.randint(2, 5)))
            for deposit in random_deposits:
                deposit.interest_user.add(user)

        self.stdout.write(self.style.SUCCESS('랜덤 찜 관계 생성 완료!'))
