from django.shortcuts import render



def AdminHomeView(request):
    context = {
        'website_header_title': 'Trang chu',
    }
    return render(request, 'frontend/admin/index.html', context)
