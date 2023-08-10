from django.shortcuts import render,redirect
from .models import Source, UserIncome
from django.core.paginator import Paginator
from userpreferences.models import UserPreference
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import json
import datetime
from django.http import JsonResponse
from collections import defaultdict
from django.db.models import Sum 
from django.http import JsonResponse, HttpResponse
import csv
import xlwt

# Create your views here.


def search_income(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        income = UserIncome.objects.filter(
            amount__istartswith = search_str, owner=request.user) | UserIncome.objects.filter(
            date__istartswith = search_str, owner=request.user) | UserIncome.objects.filter(
            description__icontains = search_str, owner=request.user) | UserIncome.objects.filter(
            source__icontains = search_str, owner=request.user)
            
        data = income.values()


        return JsonResponse(list(data), safe=False)
    




@login_required(login_url='/authentication/login')
def index(request):
    source=Source.objects.all()
    income = UserIncome.objects.filter(owner=request.user)
    paginator = Paginator(income, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    exists = UserPreference.objects.filter(user=request.user).exists()
    if exists:
        currency = UserPreference.objects.get(user=request.user).currency
    
        context = {
            'income' : income,
            'page_obj' : page_obj,
            'currency' : currency
        }
    else:
        context = {
            'income' : income,
            'page_obj' : page_obj
        }
   
    return render(request,'income/index.html', context)

def add_income(request):
    sources=Source.objects.all()
    context = {
          'sources': sources,
          'values': request.POST
    }
    if request.method == 'GET':
        return render(request,'income/add_income.html', context)

    if request.method =='POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request,'Amount is required')
            return render(request,'income/add_income.html', context)
        
        description = request.POST['description']
        date = request.POST['income_date']
        source = request.POST['source']

        if not description:
            messages.error(request,'Description is required')
            return render(request,'income/add_expenses.html', context)
        


        UserIncome.objects.create(owner=request.user,amount=amount,source=source,description=description,date=date)

        messages.success(request,'Income saved successfully')

        return redirect('income')
   

 
def income_edit(request, id):
    income=UserIncome.objects.get(pk=id)
    sources=Source.objects.all()

    context = {
        'income' : income,
        'values' : income,
        'sources' : sources,
    }
    if request.method == 'GET':
        
        return render(request, 'income/edit_income.html', context)
    if request.method =='POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request,'Amount is required')
            return render(request,'income/edit_income.html', context)
        
        description = request.POST['description']
        date = request.POST['income_date']
        source = request.POST['source']

        if not description:
            messages.error(request,'Description is required')
            return render(request,'income/edit_income.html', context)
        

        income.amount=amount
        income.source=source
        income.description=description
        income.date=date

        income.save()

        messages.success(request,'Income Updated successfully')

        return redirect('income')
    

def delete_income(request, id):
    income=UserIncome.objects.get(pk=id)
    income.delete()

    messages.success(request, 'Income deleted')
    return redirect('income')    

def income_source_summary(request):
    todays_date = datetime.date.today()
    six_months_ago = todays_date - datetime.timedelta(days = 180)
    income = UserIncome.objects.filter(owner=request.user, date__gte=six_months_ago, date__lte= todays_date)

    finalrep = {}

    def get_source(income):
        return income.source
    
    source_list = list(set(map(get_source, income)))
    def get_income_source_amount(source):
        amount = 0 
        filtered_by_source = UserIncome.objects.filter(source=source)
        
        for item in filtered_by_source:
            amount+=item.amount
        
        return amount
    
    for x in income:
        for y in source_list:
            finalrep[y]=get_income_source_amount(y)

    return JsonResponse({'income_source_data': finalrep},safe = False)

def income_source_monthly_summary(request):
    finalrep = defaultdict(list)
    today = datetime.date.today()
    one_year_ago = today - datetime.timedelta(days=365)

# Retrieve the data and group it by month
    data = UserIncome.objects.filter(owner=request.user,date__gte=one_year_ago).annotate(
        month=Sum('amount', distinct=True),
        ).values('month', 'date__month', 'date__year').order_by('date__month')
    
# Print the data for each month
    for item in data:
        datee = str(item['date__month']) +"-" +str(item['date__year'])
        finalrep[datee].append([item['month']])

    return JsonResponse({'income_source_monthly_data': finalrep},safe = False)

#last 7 days
def income_source_lastweek_summary(request):
    finalrep = defaultdict(list)
    today = datetime.date.today()
    week = today - datetime.timedelta(days=7)
    dates = [week + datetime.timedelta(days=i) for i in range(7)]

# Retrieve the data and group it by month
    data = UserIncome.objects.filter(owner=request.user,date__gte=week).annotate(
        a=Sum('amount', distinct=True),
        ).values('a','date').order_by('date')
    d = []
    for date in dates:
        amount = 0
        for daily_amount in data:   
            if daily_amount['date'] == date:
                amount = daily_amount['a']
                break
        d.append(amount)
        
# Print the data for each month
    for j in range(0,7):
        finalrep[str(dates[j])].append(d[j])


    return JsonResponse({'income_source_lastweek_data': finalrep},safe = False)


def income_stats_view(request):
    todays_date = datetime.date.today()

    #Income Today
    income_today = UserIncome.objects.filter(owner=request.user, date__gte=todays_date, date__lte= todays_date)
    income_today_count = income_today.count()
    amount_today = 0
    for item in income_today:
        amount_today+=item.amount
    
    #One Month Income
 
    one_months_ago = todays_date - datetime.timedelta(days = 30)
    income_one_months = UserIncome.objects.filter(owner=request.user, date__gte=one_months_ago, date__lte= todays_date)
    amount_one_months = 0
    income_one_months_count = income_one_months.count()

    for item in income_one_months:
        amount_one_months+=item.amount

    #Six Months Income
    six_months_ago = todays_date - datetime.timedelta(days = 180)
    income_six_months = UserIncome.objects.filter(owner=request.user, date__gte=six_months_ago, date__lte= todays_date)
    amount_six_months = 0
    income_six_months_count = income_six_months.count()

    for item in income_six_months:
        amount_six_months+=item.amount

     #12 Months Income
    year_ago = todays_date - datetime.timedelta(days = 365)
    income_year = UserIncome.objects.filter(owner=request.user, date__gte=year_ago, date__lte= todays_date)
    amount_year = 0
    income_year_count = income_year.count()

    for item in income_year:
        amount_year+=item.amount
    context = {
        'amount_today' : amount_today,
        'income_today_count' : income_today_count,
        'amount_six_months' : amount_six_months,
        'income_six_months_count' : income_six_months_count,
        'amount_one_months' : amount_one_months,
        'income_one_months_count' : income_one_months_count,
        'amount_year' : amount_year,
        'income_year_count' : income_year_count,
    }
    return render(request, 'income/incomestats.html', context)

def export_csv(request):
    response = HttpResponse(content_type = 'text/csv')
    response['content-Disposition']='attachment; filename=Expenses'+str(datetime.datetime.now())+'.csv'

    writer = csv.writer(response)
    writer.writerow(['Amount','Description','Category','Date'])

    income = UserIncome.objects.filter(owner=request.user)

    for i in income:
        writer.writerow([i.amount,i.description,i.source,i.date])

    return response


def export_excel(request):
    response = HttpResponse(content_type = 'application/ms-excel')
    response['content-Disposition']='attachment; filename=Expenses'+str(datetime.datetime.now())+'.xls'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Expenses')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
     
    columns = ['Amount','Description','Source','Date']

    for col_num in range(len(columns)):
        ws.write(row_num,col_num,columns[col_num],font_style)

    font_style = xlwt.XFStyle()

    rows=UserIncome.objects.filter(owner=request.user).values_list('amount','description','source','date')

    for row in rows:
        row_num+=1

        for col_num in range(len(row)):
            ws.write(row_num,col_num,str(row[col_num]),font_style)

    wb.save(response)

    return response

    
        