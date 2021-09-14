from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from backend.models.language import LanguageModel
import sys
import inspect

from judger.grader import *

class Command(BaseCommand):

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Đặt lại & cập nhật mọi cài đặt trình chấm bài',
        )
        super().add_arguments(parser)

    def handle(self, *args, **options):
        if not options['reset']:
            print('\nSử dụng python manage.py grader --reset để đặt lại mọi cài đặt về trình chấm bài\n')
            return
        
        #test
        list_language_class_name = []
        list_language_name = []
        for class_name, obj in inspect.getmembers(sys.modules[__name__]):
            if inspect.isclass(obj) and issubclass(obj, GraderAbstract) and obj is not GraderAbstract:
                if len(obj._name) == 0:
                    return 'Lỗi: class {} không có tên ngôn ngữ'.format(obj.__name__)
                if len(obj._extension) == 0:
                    return 'Lỗi: class {} không có extension'.format(obj.__name__)
                if len(obj._run_command) == 0:
                    return 'Lỗi: class {} không có lệnh chạy (run command)'.format(obj.__name__)
                if len(obj._execute_name) == 0:
                    return 'Lỗi: class {} không có tên file thực thi'.format(obj.__name__)
                if obj._name in list_language_name:
                    return 'Lỗi: Có nhiều hơn 1 ngôn ngữ với _name: \'{}\''.format(obj._name)
                list_language_name.append(obj._name)
                if class_name in list_language_class_name:
                    return 'Lỗi: Có nhiều hơn 1 ngôn ngữ với tên class: \'{}\''.format(class_name)
                list_language_class_name.append(class_name)
        
        for entry in LanguageModel.objects.filter().all():
            if entry.class_name not in list_language_class_name:
                print('- Xóa ngôn ngữ: class={}, name={}'.format(entry.class_name, entry.name))
                entry.delete()

        for name, obj in inspect.getmembers(sys.modules[__name__]):
            if inspect.isclass(obj) and issubclass(obj, GraderAbstract) and obj is not GraderAbstract:
                    entries = LanguageModel.objects.filter(class_name=name)
                    if not entries.exists():
                        entry = LanguageModel.objects.create(
                            class_name=name,
                            name=obj._name,
                            ext=obj._extension,
                            compile_command=obj._compiler_command,
                            run_command=obj._run_command,
                            description=obj._description,
                            execute_name=obj._execute_name)
                        entry.save()
                        print('+ Thêm ngôn ngữ: class={}, name={}'.format(entry.class_name, entry.name))
                    else:
                        for entry in entries:
                            print('# Cập nhật ngôn ngữ: class={}, name={}'.format(entry.class_name, entry.name))
                            entry.class_name = name
                            entry.name = obj._name
                            entry.ext = obj._extension
                            entry.compile_command = obj._compiler_command
                            entry.run_command = obj._run_command
                            entry.description = obj._description
                            entry.execute_name = obj._execute_name
                            entry.save()
        


