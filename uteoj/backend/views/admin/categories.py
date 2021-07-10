from django.shortcuts import render
from django.http import HttpResponse
from backend.models.problem import ProblemCategoryModel
from backend.views.admin.require import admin_member_required

import json

@admin_member_required
def AdminCategoriesView(request):
    context = {
        'list_categories': [
            {
                'id': x.id,
                'name': x.name,
                'description': x.description,
            }
            for x in ProblemCategoryModel.objects.all()]
    }
    if request.method == 'POST':
        print(request.POST)
        if 'method' not in request.POST:
            return HttpResponse(status=500)
        method = request.POST['method']
        response_data = { }
        if method == 'add':
            if 'name' not in request.POST or 'description' not in request.POST:
                return HttpResponse(status=500)
            name = request.POST['name']
            description = request.POST['description']
            if ProblemCategoryModel.objects.filter(name=name).exists():
                response_data['status'] = 'error'
                response_data['message'] = 'Tên này đã có'
                return HttpResponse(json.dumps(response_data, indent=4), content_type="application/json")
            else:
                if len(name) == 0:
                    response_data['status'] = 'error'
                    response_data['message'] = 'Tên không được trống'
                elif name == 'All':
                    response_data['status'] = 'error'
                    response_data['message'] = 'Không được đặt tên là \'All\''
                else:
                    ProblemCategoryModel.objects.create(name=name, description=description).save()
                    response_data['status'] = 'success'
                    response_data['message'] = 'Thêm thành công'
                return HttpResponse(json.dumps(response_data, indent=4), content_type="application/json")
        elif method == 'edit':
            if 'new_name' not in request.POST or 'description' not in request.POST or 'old_name' not in request.POST:
                return HttpResponse(status=500)
            new_name = request.POST['new_name']
            description = request.POST['description']
            old_name = request.POST['old_name']
            if ProblemCategoryModel.objects.filter(name=new_name).exists():
                response_data['status'] = 'error'
                response_data['message'] = 'Tên này đã có'
                return HttpResponse(json.dumps(response_data, indent=4), content_type="application/json")
            else:
                if len(new_name) == 0:
                    response_data['status'] = 'error'
                    response_data['message'] = 'Tên không được trống'
                elif new_name == 'All':
                    response_data['status'] = 'error'
                    response_data['message'] = 'Không được đặt tên là \'All\''
                else:
                    category = ProblemCategoryModel.objects.filter(name=old_name)[0]
                    category.name = new_name
                    category.description = description
                    category.save()
                    response_data['status'] = 'success'
                    response_data['message'] = 'Sửa thành công'
                return HttpResponse(json.dumps(response_data, indent=4), content_type="application/json")
        elif method == 'delete':
            if 'name' not in request.POST:
                return HttpResponse(status=500)
            name = request.POST['name']
            ProblemCategoryModel.objects.filter(name=name).delete()
            response_data['status'] = 'success'
            response_data['message'] = 'Xóa thành công'
            return HttpResponse(json.dumps(response_data, indent=4), content_type="application/json")
        else:
            response_data['status'] = 'error'
            response_data['message'] = 'Unknown method'
            return HttpResponse(json.dumps(response_data, indent=4), content_type="application/json")
    return render(request, 'admin-template/category/category.html', context)

