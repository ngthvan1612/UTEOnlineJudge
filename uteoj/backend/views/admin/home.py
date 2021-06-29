from django.shortcuts import render



def AdminHomeView(request):
    context = {
        'website_header_title': 'Trang chu',
    }
    return render(request, 'admin-template/html/index.html', context)
