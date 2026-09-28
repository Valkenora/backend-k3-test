from django.shortcuts import render

def login_view(request):
    return render(request, 'she/login.html')

def dashboard_view(request):
    return render(request, 'she/dashboard.html')

def hira_list_view(request):
    return render(request, 'she/hira_list.html')

def hira_create_view(request):
    return render(request, 'she/hira_create.html')

def ptw_list_view(request):
    return render(request, 'she/ptw_list.html')

def ptw_create_view(request):
    return render(request, 'she/ptw_create.html')