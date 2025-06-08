from django.core.management.base import BaseCommand
import pandas as pd
from golds.models import PriceData
from datetime import datetime
import os

class Command(BaseCommand):
    help = 'Load price data from Excel files'

    def handle(self, *args, **kwargs):
        # 현재 앱 디렉토리 경로
        app_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        
        # Gold 데이터 로드
        gold_file = os.path.join(app_dir, 'Gold_prices.xlsx')
        if os.path.exists(gold_file):
            self.stdout.write(f'Reading gold file: {gold_file}')
            gold_df = pd.read_excel(gold_file)
            self.stdout.write(f'Gold data columns: {gold_df.columns.tolist()}')
            self.stdout.write(f'First row of gold data: {gold_df.iloc[0].to_dict()}')
            
            for _, row in gold_df.iterrows():
                try:
                    date = pd.to_datetime(row['Date']).date()
                    price = float(str(row['Close/Last']).replace(',', ''))
                    PriceData.objects.get_or_create(
                        date=date,
                        asset_type='GOLD',
                        defaults={'price': price}
                    )
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error processing gold row: {row}, Error: {str(e)}'))
            
            self.stdout.write(self.style.SUCCESS(f'Successfully loaded gold prices'))
        else:
            self.stdout.write(self.style.WARNING(f'Gold price file not found at {gold_file}'))

        # Silver 데이터 로드
        silver_file = os.path.join(app_dir, 'Silver_prices.xlsx')
        if os.path.exists(silver_file):
            self.stdout.write(f'Reading silver file: {silver_file}')
            silver_df = pd.read_excel(silver_file)
            self.stdout.write(f'Silver data columns: {silver_df.columns.tolist()}')
            self.stdout.write(f'First row of silver data: {silver_df.iloc[0].to_dict()}')
            
            for _, row in silver_df.iterrows():
                try:
                    date = pd.to_datetime(row['Date']).date()
                    price = float(str(row['Close/Last']).replace(',', ''))
                    PriceData.objects.get_or_create(
                        date=date,
                        asset_type='SILVER',
                        defaults={'price': price}
                    )
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error processing silver row: {row}, Error: {str(e)}'))
            
            self.stdout.write(self.style.SUCCESS(f'Successfully loaded silver prices'))
        else:
            self.stdout.write(self.style.WARNING(f'Silver price file not found at {silver_file}')) 