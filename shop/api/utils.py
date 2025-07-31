
from shop.models import Customer , Company
import random
from datetime import date, timedelta
from django.db.models import Count
from shop.models import CustomerPackages , Analytics


def generate_unique_number():
    return random.randint(1000000, 9999990)

def get_unique_number():
    value = generate_unique_number()
    while Customer.objects.filter(customer_id=value).exists():
        value = generate_unique_number()
    return value

def get_unique_number_vendor():
    value = generate_unique_number()
    while Company.objects.filter(vendor_id=value).exists():
        value = generate_unique_number()
    return value

def calculate_sales_percentage():
    # Get today's date
    today = date.today()

    # Calculate yesterday's date
    yesterday = today - timedelta(days=1)

    # Retrieve count of sales for today and yesterday
    sales_today = CustomerPackages.objects.filter(purchase_date=today).count()
    sales_yesterday = CustomerPackages.objects.filter(purchase_date=yesterday).count()

    # Calculate percentage increase or decrease
    if sales_yesterday == 0:
        sales_percentage = 100  # Handle division by zero if there were no sales yesterday
    else:
        sales_percentage = ((sales_today - sales_yesterday) / sales_yesterday) * 100

    return sales_percentage

def get_join_counts():
    # Get today's date
    today = date.today()

    # Get the start and end dates for this week
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    # Get the start and end dates for this month
    start_of_month = date(today.year, today.month, 1)
    if today.month == 12:  # Handle December separately
        end_of_month = date(today.year + 1, 1, 1) - timedelta(days=1)
    else:
        end_of_month = date(today.year, today.month + 1, 1) - timedelta(days=1)

    # Count of companies joined today
    companies_today = Company.objects.filter(join_date=today).count()

    # Count of companies joined this week
    companies_this_week = Company.objects.filter(join_date__range=[start_of_week, end_of_week]).count()

    # Count of companies joined this month
    companies_this_month = Company.objects.filter(join_date__range=[start_of_month, end_of_month]).count()

    return {
        'today': companies_today,
        'this_week': companies_this_week,
        'this_month': companies_this_month
    }

def calculate_join_percentage():
    # Get today's date
    today = date.today()

    # Calculate yesterday's date
    yesterday = today - timedelta(days=1)

    # Retrieve count of sales for today and yesterday
    sales_today = Company.objects.filter(join_date=today).count()
    sales_yesterday = Company.objects.filter(join_date=yesterday).count()

    # Calculate percentage increase or decrease
    if sales_yesterday == 0:
        sales_percentage = 100
    else:
        sales_percentage = ((sales_today - sales_yesterday) / sales_yesterday) * 100

    return sales_percentage
