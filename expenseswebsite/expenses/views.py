from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Expense
from django.contrib import messages
from django.core.paginator import Paginator
import json
from django.http import JsonResponse, HttpResponse
from userpreferences.models import UserPreference
import datetime
import csv
import xlwt
from collections import defaultdict
from django.db.models import Sum 

# Create your views here.

def search_expenses(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        expenses = Expense.objects.filter(
            amount__istartswith = search_str, owner=request.user) | Expense.objects.filter(
            date__istartswith = search_str, owner=request.  user) | Expense.objects.filter(
            description__icontains = search_str, owner=request.user) | Expense.objects.filter(
            category__icontains = search_str, owner=request.user)
            
        data = expenses.values()


        return JsonResponse(list(data), safe=False)
    






@login_required(login_url='/authentication/login')
def index(request):
    categories=Category.objects.all()
    expenses = Expense.objects.filter(owner=request.user)
    paginator = Paginator(expenses, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    exists = UserPreference.objects.filter(user=request.user).exists()
    if exists:
        currency = UserPreference.objects.get(user=request.user).currency
    
        context = {
            'expenses' : expenses,
            'page_obj' : page_obj,
            'currency' : currency
        }
    else:
        context = {
            'expenses' : expenses,
            'page_obj' : page_obj
        }
    return render(request,'expenses/index.html', context)

def add_expense(request):
    categories=Category.objects.all()
    context = {
          'categories': categories,
          'values': request.POST
    }
    if request.method == 'GET':
        return render(request,'expenses/add_expenses.html', context)

    if request.method =='POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request,'Amount is required')
            return render(request,'expenses/add_expenses.html', context)
        
        description = request.POST['description']
        date = request.POST['expense_date']
        category = request.POST['category']

        if not description:
            messages.error(request,'Description is required')
            return render(request,'expenses/add_expenses.html', context)
        


        Expense.objects.create(owner=request.user,amount=amount,category=category,description=description,date=date)

        messages.success(request,'Expense saved successfully')

        return redirect('expenses')
    
def expense_edit(request, id):
    expense=Expense.objects.get(pk=id)
    categories=Category.objects.all()

    context = {
        'expense' : expense,
        'values' : expense,
        'categories' : categories,
    }
    if request.method == 'GET':
        
        return render(request, 'expenses/edit-expenses.html', context)
    if request.method =='POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request,'Amount is required')
            return render(request,'expenses/edit_expenses.html', context)
        
        description = request.POST['description']
        date = request.POST['expense_date']
        category = request.POST['category']

        if not description:
            messages.error(request,'Description is required')
            return render(request,'expenses/edit_expenses.html', context)
        

        expense.owner=request.user
        expense.amount=amount
        expense.category=category
        expense.description=description
        expense.date=date

        expense.save()

        messages.success(request,'Expense Updated successfully')

        return redirect('expenses')
    

def delete_expense(request, id):
    expense=Expense.objects.get(pk=id)
    expense.delete()

    messages.success(request, 'Expense deleted')
    return redirect('expenses')    


def expense_category_summary(request):
    todays_date = datetime.date.today()
    six_months_ago = todays_date - datetime.timedelta(days = 180)
    expenses = Expense.objects.filter(owner=request.user, date__gte=six_months_ago, date__lte= todays_date)

    finalrep = {}

    def get_category(expense):
        return expense.category
    
    category_list = list(set(map(get_category, expenses)))
    def get_expense_category_amount(category):
        amount = 0 
        filtered_by_category = expenses.filter(category=category)
        
        for item in filtered_by_category:
            amount+=item.amount


        return amount
    
    for x in expenses:
        for y in category_list:
            finalrep[y]=get_expense_category_amount(y)


    return JsonResponse({'expense_category_data': finalrep},safe = False)

def stats_view(request):
    todays_date = datetime.date.today()
    #Today
    today = Expense.objects.filter(owner=request.user, date__gte=todays_date, date__lte= todays_date)
    today_count = today.count()
    amount_today = 0
    for item in today:
        amount_today += item.amount
    
    #One Month  
    one_months_ago = todays_date - datetime.timedelta(days = 30)
    one_months = Expense.objects.filter(owner=request.user, date__gte=one_months_ago, date__lte= todays_date)
    amount_one_months = 0
    one_months_count = one_months.count()

    for item in one_months:
        amount_one_months+=item.amount

    #Six Months     
    six_months_ago = todays_date - datetime.timedelta(days = 180)
    six_months = Expense.objects.filter(owner=request.user, date__gte=six_months_ago, date__lte= todays_date)
    amount_six_months = 0
    six_months_count = six_months.count()

    for item in six_months:
        amount_six_months+=item.amount

     #12 Months     
    year_ago = todays_date - datetime.timedelta(days = 365)
    year = Expense.objects.filter(owner=request.user, date__gte=year_ago, date__lte= todays_date)
    amount_year = 0
    year_count = year.count()

    for item in year:
        amount_year+=item.amount
    context = {
        'amount_today' : amount_today,
        'today_count' : today_count,
        'amount_six_months' : amount_six_months,
        'six_months_count' : six_months_count,
        'amount_one_months' : amount_one_months,
        'one_months_count' : one_months_count,
        'amount_year' : amount_year,
        'year_count' : year_count,
    }
    return render(request, 'expenses/stats.html', context)



def export_csv(request):
    response = HttpResponse(content_type = 'text/csv')
    response['content-Disposition']='attachment; filename=Expenses'+str(datetime.datetime.now())+'.csv'

    writer = csv.writer(response)
    writer.writerow(['Amount','Description','Category','Date'])

    expenses = Expense.objects.filter(owner=request.user)

    for expense in expenses:
        writer.writerow([expense.amount,expense.description,expense.category,expense.date])

    return response

def export_excel(request):
    response = HttpResponse(content_type = 'application/ms-excel')
    response['content-Disposition']='attachment; filename=Expenses'+str(datetime.datetime.now())+'.xls'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Expenses')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
     
    columns = ['Amount','Description','Category','Date']

    for col_num in range(len(columns)):
        ws.write(row_num,col_num,columns[col_num],font_style)

    font_style = xlwt.XFStyle()

    rows=Expense.objects.filter(owner=request.user).values_list('amount','description','category','date')

    for row in rows:
        row_num+=1

        for col_num in range(len(row)):
            ws.write(row_num,col_num,str(row[col_num]),font_style)

    wb.save(response)

    return response



def expenses_monthly_summary(request):
    finalrep = defaultdict(list)
    today = datetime.date.today()
    one_year_ago = today - datetime.timedelta(days=365)

# Retrieve the data and group it by month
    data = Expense.objects.filter(owner=request.user,date__gte=one_year_ago).annotate(
        month=Sum('amount', distinct=True),
        ).values('month', 'date__month', 'date__year').order_by('date__month')
    
# Print the data for each month
    for item in data:
        datee = str(item['date__month']) +"-" +str(item['date__year'])
        finalrep[datee].append([item['month']])
    return JsonResponse({'expenses_monthly_data': finalrep},safe = False)

#last 7 days
def expenses_lastweek_summary(request):
    finalrep = defaultdict(list)
    today = datetime.date.today()
    week = today - datetime.timedelta(days=7)
    dates = [week + datetime.timedelta(days=i) for i in range(0,8)]

# Retrieve the data and group it by month
    data = Expense.objects.filter(owner=request.user,date__gte=week).annotate(
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
    for j in range(0,8):
        finalrep[str(dates[j])].append(d[j])


    return JsonResponse({'expenses_lastweek_data': finalrep},safe = False)




