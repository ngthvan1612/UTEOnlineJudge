from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.db import transaction
from backend.models.problem import ProblemCategoryModel, ProblemModel
from datetime import datetime
import json
from random import random

@csrf_exempt
def CreateRandomProblem(request):
    list_requirements = ['startwith', 'count']
    for x in list_requirements:
        if x not in request.GET:
            return JsonResponse({
                'status': 'error',
                'message': 'missing \'' + x + '\' parameter',
            })
    try:
        msg_error = 'startwith error'
        startwith = request.GET['startwith']
        msg_error = 'count error (must be integer)'
        count = int(request.GET['count'])
    except:
        return JsonResponse({
                'status': 'error',
                'message': msg_error
            })
    
    response = []
    with transaction.atomic():
        for i in range(1, count + 1, 1):
            num_lc = int(random() * ProblemCategoryModel.objects.count()) + 1
            lc = [x.id for x in ProblemCategoryModel.objects.order_by('?').all()[:num_lc]]

            num_uc = int(random() * User.objects.count()) + 1
            uc = [x.id for x in User.objects.order_by('?').all()[:num_uc]]
            problem = ProblemModel.objects.create(publish_date=datetime.now(),
                shortname=startwith.replace(" ", '_').upper() + str(i),
                fullname=startwith + str(i),
                difficult=round(random() * 10, 2),
                points_per_test=random() * 100,
                statement=
                "# Statement of {}\n"
                "Publishing in StackEdit makes it simple for you to publish online your files. Once you're happy with a file, you can publish it to different hosting platforms like **Blogger**, **Dropbox**, **Gist**, **GitHub**, **Google Drive**, **WordPress** and **Zendesk**. With [Handlebars templates](http://handlebarsjs.com/), you have full control over what you export.\n"
                "> Before starting to publish, you must link an account in the **Publish** sub-menu.\n".format(startwith + str(i)),
                input_statement=
                "# Input of {}\n"
                "> **ProTip:** You can disable any **Markdown extension** in the **File properties** dialog.\n".format(startwith + str(i)),
                output_statement=
                "# Output of {}\n"
                "You can render LaTeX mathematical expressions using [KaTeX](https://khan.github.io/KaTeX/):\n".format(startwith + str(i)),
                constraints_statement=
                "# Constraint of {}\n"
                "The *Gamma function* satisfying $\Gamma(n) = (n-1)!\quad\forall n\in\mathbb N$ is via the Euler integral\n".format(startwith + str(i)),
                input_filename='BAI' + str(i) + '.INP',
                output_filename='BAI' + str(i) + '.OUT',
                time_limit=int(random() * 10000),
                memory_limit=int(random() * 1000000),
                problem_type=int(random() * 2),)
            problem.set_categories(lc)
            problem.author.set(uc)
            problem.save()
    return HttpResponse('Created ' + str(count) + ' problem ok')

