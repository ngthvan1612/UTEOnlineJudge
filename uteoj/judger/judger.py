# File này phải chạy trên quyền root

from backend.models.submission import SubmissionModel
from backend.models.submission import SubmissionTestcaseResultModel
from backend.models.language import LanguageModel

from backend.models.filemanager import OverwriteStorage
from django.core.files.base import ContentFile
from backend.models.submission import SubmissionResultType

from django.conf import settings
import uuid
import os
import shutil
import time
import subprocess
from subprocess import check_output
from subprocess import PIPE

import json
import subprocess

UNLIMITED = -1
VERSION = 0x020101

RESULT_SUCCESS = 0
RESULT_WRONG_ANSWER = -1
RESULT_CPU_TIME_LIMIT_EXCEEDED = 1
RESULT_REAL_TIME_LIMIT_EXCEEDED = 2
RESULT_MEMORY_LIMIT_EXCEEDED = 3
RESULT_RUNTIME_ERROR = 4
RESULT_SYSTEM_ERROR = 2

ERROR_INVALID_CONFIG = -1
ERROR_FORK_FAILED = -2
ERROR_PTHREAD_FAILED = -3
ERROR_WAIT_FAILED = -4
ERROR_ROOT_REQUIRED = -5
ERROR_LOAD_SECCOMP_FAILED = -6
ERROR_SETRLIMIT_FAILED = -7
ERROR_DUP2_FAILED = -8
ERROR_SETUID_FAILED = -9
ERROR_EXECVE_FAILED = -10
ERROR_SPJ_ERROR = -11


def run(max_cpu_time,
        max_real_time,
        max_memory,
        max_stack,
        max_output_size,
        max_process_number,
        exe_path,
        input_path,
        output_path,
        error_path,
        args,
        env,
        log_path,
        seccomp_rule_name,
        uid,
        gid,
        memory_limit_check_only=0):
    str_list_vars = ["args", "env"]
    int_vars = ["max_cpu_time", "max_real_time",
                "max_memory", "max_stack", "max_output_size",
                "max_process_number", "uid", "gid", "memory_limit_check_only"]
    str_vars = ["exe_path", "input_path", "output_path", "error_path", "log_path"]

    proc_args = ["/usr/lib/judger/libjudger.so"]

    for var in str_list_vars:
        value = vars()[var]
        if not isinstance(value, list):
            raise ValueError("{} must be a list".format(var))
        for item in value:
            if not isinstance(item, str):
                raise ValueError("{} item must be a string".format(var))
            proc_args.append("--{}={}".format(var, item))

    for var in int_vars:
        value = vars()[var]
        if not isinstance(value, int):
            raise ValueError("{} must be a int".format(var))
        if value != UNLIMITED:
            proc_args.append("--{}={}".format(var, value))

    for var in str_vars:
        value = vars()[var]
        if not isinstance(value, str):
            raise ValueError("{} must be a string".format(var))
        proc_args.append("--{}={}".format(var, value))

    if not isinstance(seccomp_rule_name, str) and seccomp_rule_name is not None:
        raise ValueError("seccomp_rule_name must be a string or None")
    if seccomp_rule_name:
        proc_args.append("--seccomp_rule={}".format(seccomp_rule_name))

    proc = subprocess.Popen(proc_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    if err:
        raise ValueError("Error occurred while calling judger: {}".format(err))
    return json.loads(out.decode("utf-8"))


def Compile(submission:SubmissionModel):
    """
    submission: Bài gửi lên (gửi cả model)

    $SOURCE_NAME$ : tên của file (không bao gồm extension)
    $SOURCE_NAME_EXT$ : tên của file (bao gồm cả extension)

    $EXECUTE_NAME$ : tên file thực thi (không bao gồm ext)
    $EXECUTE_NAME_EXT$ : tên file thực thi (bao gồm ext)

    """
    language = submission.language
    file_manager = OverwriteStorage(settings.COMPILE_ROOT)
    
    #Lưu bài vào ổ đĩa
    ## ../compile/{hash md5 - shuffle name}/Main<lang ext>
    random_md5 = str(uuid.uuid4().hex) + '_' + str(submission.pk)
    file_name = os.path.join(random_md5, 'Main' + language.ext)
    try:
        file_manager.save(file_name, ContentFile(submission.source_code))
    except:
        try:
            shutil.rmtree(os.path.join(settings.COMPILE_ROOT, random_md5))
        except:
            pass
        return [False, SubmissionResultType.CE, '']

    #Biên dịch
    if len(language.compile_command) == 0:
        return [True, file_name, ''] # Trường hợp này không cần biên dịch

    try:
        raw_command = language.compile_command
        raw_command = raw_command.replace('$SOURCE_NAME$', 'Main')
        raw_command = raw_command.replace('$SOURCE_NAME_EXT$', 'Main' + language.ext)
        command = [x for x in raw_command.split() if len(x)]
        process = subprocess.Popen(command, cwd=os.path.join(settings.COMPILE_ROOT, random_md5), stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, error = process.communicate()
        output = output.decode('utf-8')
        error = error.decode('utf-8')
        print('OUTPUT => ' + output)
        print('ERROR => ' + error)
        if process.returncode != 0:
            print('Dịch lỗi rồi :((( ' + str(process.returncode))
            return [False, SubmissionResultType.CE, error]
    except Exception as e:
        return [False, SubmissionResultType.CE, error]
    print('Dịch thành công :)))')


    #Debug, chạy xong hết test rồi xóa
    try:
        shutil.rmtree(os.path.join(settings.COMPILE_ROOT, random_md5))
    except:
        pass
    
    return [True, file_name, output]

"""
ret = _judger.run(max_cpu_time=1000,
                  max_real_time=5000,
                  max_memory=1 * 1024 * 1024,
                  max_process_number=200,
                  max_output_size=10000,
                  max_stack=_judger.UNLIMITED,
                  exe_path="main",
                  input_path="1.in",
                  output_path="1.out",
                  error_path="1.out",
                  args=[],
                  # can be empty list
                  env=[],
                  log_path="judger.log",
                  # can be None
                  seccomp_rule_name=None,
                  uid=0,
                  gid=0)
"""

def RunTest(submission):

    return [True]
