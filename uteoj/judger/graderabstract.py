from abc import abstractclassmethod, ABC, abstractmethod
import subprocess
import os
from genericpath import exists
from posixpath import commonpath
from re import sub
from typing import Tuple, overload
from subprocess import check_output
from django.conf import settings

from django.utils import timezone
from django.db import transaction

from backend.models.submission import SubmissionResultType, SubmissionStatusType, SubmissionModel, SubmissionTestcaseResultModel
from backend.models.usersetting import UserProblemStatisticsModel
from backend.models.problem import ProblemStatisticsModel, ProblemType

from judger.score import ACMScore, OIScore
from judger import judger

class GraderAbstract(ABC):

    _name = ''
    _extension = ''
    _compiler_command = ''
    _run_command = ''
    _execute_name = ''
    _compiler_workdir = ''
    _run_workdir = ''
    _source_file_name = ''
    _description = ''

    def __init__(self, compiler_workdir, run_workdir) -> None:
        self._compiler_workdir = compiler_workdir
        self._run_workdir = run_workdir

    def _prepare(self, source_code):
        #write
        open(os.path.join(self._compiler_workdir, 'main' + self._extension), 'w', encoding='utf-8').write(source_code)
        self._source_file_name = 'main' + self._extension

    def _compileSource(self):
        file_name_without_ext, ext = os.path.splitext(self._source_file_name)
        command_parse = {
            '$SOURCE_NAME_EXT$': self._source_file_name,
            '$SOURCE_NAME$': file_name_without_ext,
            '$EXT$': ext
        }
        temp = self._compiler_command
        for key, value in command_parse.items():
            temp = temp.replace(key, value)
        command = [x for x in temp.split(' ') if len(x) > 0]

        process = subprocess.Popen(command, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE, cwd=self._compiler_workdir)
        process_stdout, process_stderr = process.communicate()
        process_stdout = process_stdout.decode('utf-8')
        process_stderr = process_stderr.decode('utf-8')
        exit_code = process.returncode

        if exit_code == 0:
            # Success
            return (SubmissionStatusType.Grading, None, '')
        
        #Failed
        return (SubmissionStatusType.Completed, SubmissionResultType.CE, process_stderr)

    @staticmethod    
    def compileChecker(problem_dir):
        raw_command = '/usr/bin/g++ -std=c++14 -O2 -Wall checker.cpp -o checker.tmp'
        command = [x for x in raw_command.split() if x]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE, cwd=os.path.join(problem_dir, 'checker'))
        process_stdout, process_stderr = process.communicate()
        process_stdout = process_stdout.decode('utf-8')
        process_stderr = process_stderr.decode('utf-8')
        exit_code = process.returncode

        if exit_code == 0:
            # Success
            os.system('rm -rf ' + os.path.join(problem_dir, 'checker', 'checker'))
            os.rename(os.path.join(problem_dir, 'checker', 'checker.tmp'), os.path.join(problem_dir, 'checker', 'checker'))
            return (True, '')
        
        #Failed
        return (False, process_stderr)
    
    def _copyExecute(self, dest):
        file_name_without_ext, ext = os.path.splitext(self._source_file_name)
        command_parse = {
            '$SOURCE_NAME_EXT$': self._source_file_name,
            '$SOURCE_NAME$': file_name_without_ext,
            '$EXT$': ext,
        }
        exe = self._execute_name
        for key, value in command_parse.items():
            exe = exe.replace(key, value)
        
        os.system('cp ' + os.path.join(self._compiler_workdir, exe) + ' ' + dest)

    def _predict(self, input, output, workDir, time_limit, mem_limit) -> Tuple[bool, str, int, int, int]:
        file_name_without_ext, ext = os.path.splitext(self._source_file_name)
        command_parse = {
            '$SOURCE_NAME_EXT$': self._source_file_name,
            '$SOURCE_NAME$': file_name_without_ext,
            '$EXT$': ext
        }
        temp = self._run_command
        for key, value in command_parse.items():
            temp = temp.replace(key, value)
        command = [x for x in temp.split(' ') if x]

        ret = judger.run(max_cpu_time=time_limit,
                max_real_time=time_limit,
                max_memory=mem_limit * 1024,
                max_process_number=200,
                max_output_size=10000,
                max_stack=mem_limit * 1024,
                exe_path=command[0],
                input_path=input,
                output_path=output + '',
                error_path='/dev/null',
                args=command[1:],
                env=[],
                log_path='/dev/null',
                seccomp_rule_name=None,
                uid=settings.RUN_UID,
                gid=settings.RUN_GID,
                workDir=workDir,
                memory_limit_check_only=1)
        
        cpu_time = ret['cpu_time']
        memory = ret['memory'] // 1024
        exit_code = ret['exit_code']
        result = ret['result']
        if result == judger.RESULT_SUCCESS:
            # ok
            return (True, SubmissionResultType.AC, cpu_time, memory, exit_code)
        if result == judger.RESULT_CPU_TIME_LIMIT_EXCEEDED or result == judger.RESULT_REAL_TIME_LIMIT_EXCEEDED:
            #chạy quá thời gian
            return (False, SubmissionResultType.TLE, cpu_time, memory, exit_code)
        if result == judger.RESULT_MEMORY_LIMIT_EXCEEDED:
            #vượt quá bộ nhớ
            return (False, SubmissionResultType.MLE, cpu_time, memory, exit_code)
        if result == judger.RESULT_SYSTEM_ERROR:
            #lỗi hệ thống
            return (False, SubmissionResultType.SYS_ERROR, cpu_time, memory, exit_code)
        #chạy sinh lỗi
        return (False, SubmissionResultType.RTE, cpu_time, memory, exit_code)

    def grading(self,
                submission_id:int,
                source_code:str,
                problem_dir:str,
                input_file:str,
                output_file:str,
                time_limit:int,
                memory_limit:int,
                use_stdin:bool,
                use_stdout:bool,
                use_external_checker:bool,
                problem_type:int) -> Tuple[int, int, int, int, int]:
        submission = SubmissionModel.objects.get(pk=submission_id)
        problem = submission.problem
        user = submission.user
        
        if problem_type == ProblemType.ACM:
            scorer = ACMScore(user, problem)
        elif problem_type == ProblemType.OI:
            scorer = OIScore(user, problem)
        else:
            raise Exception('Unknown problem_type: ' + str(problem_type))

        # BIÊN DỊCH -------------------------------------------------------------------------------------
        submission.submission_judge_date = timezone.localtime(timezone.now())
        submission.save()

        with transaction.atomic():
            problemStatisticsEntries = ProblemStatisticsModel.objects.select_for_update().filter(problem=problem)
            for problemStatistics in problemStatisticsEntries:
                problemStatistics.totalSubmission = problemStatistics.totalSubmission + 1
                problemStatistics.save()
        
        with transaction.atomic():
            UserProblemStatisticsModel.createStatIfNotExists(user)
            userStatisticEntries = UserProblemStatisticsModel.objects.select_for_update().filter(user=user)
            for stat in userStatisticEntries:
                stat.totalSubmission = stat.totalSubmission + 1
                stat.save()

        self._prepare(source_code)
        status, result, compile_err = self._compileSource()

        if result == SubmissionResultType.CE: # DỊCH LỖI ------------------------------------------------
            scorer.onCompileError()
            submission.result = SubmissionResultType.CE # Dịch lỗi
            submission.status = SubmissionStatusType.Completed # Xong
            submission.compile_message = compile_err
            submission.save()
            scorer.onCompleted()
            return (status, result, 0, 0, compile_err)
        
        # CHẤM BÀI -------------------------------------------------------------------------------------
        # Copy all tests to dest
        submission.status = SubmissionStatusType.Grading
        submission.save()
        os.system('cp -Rf ' + os.path.join(problem_dir, 'tests', '*') + ' ' + self._run_workdir)

        # Chạy test
        currentTestId = 1
        numberOfAC = 0
        sumMemoryUsage = 0
        sumExecuteTime = 0
        for testcase in problem.problemtestcasemodel_set.all():
            if not scorer.canContinue():
                break

            submission.lastest_test = currentTestId
            currentTestId = currentTestId + 1
            submission.save()
            testdir = os.path.join(self._run_workdir, testcase.input_file.split('/')[3])

            # Đổi tên output của bài lại (thêm .answer)
            os.rename(os.path.join(testdir, output_file), os.path.join(testdir, output_file) + '.answer')
            
            # Copy file chạy vô thư mục test hiện tại
            self._copyExecute(testdir)

            # Fix lại input, output -> Chạy
            input_fixed = input_file if use_stdin else '/dev/null'
            output_fixed = output_file if use_stdout else '/dev/null'
            time_limit_fixed = max(int(time_limit) // 10 * 10 - 5, 1)
            ret, result, execute_time, memory_usage, exit_code = self._predict(input_fixed, output_fixed, testdir, time_limit_fixed, memory_limit)

            # Xử lý kết quả
            submission_result = SubmissionTestcaseResultModel.objects.create(testcase=testcase,submission=submission,executed_time=execute_time,memory_usage=memory_usage,points=0.0)
            if result == SubmissionResultType.AC:
                if use_external_checker:
                    # Dùng trình chấm ngoài
                    checker = os.path.join(problem_dir, 'checker', 'checker')
                    checker = os.path.abspath(checker)
                    command = [checker, input_file, output_file, output_file + '.answer']
                else:
                    # Dùng diff của linux, --> cần fix lại
                    checker = '/usr/bin/diff'
                    command = [checker, '--strip-trailing-cr', output_file, output_file + '.answer']
                
                # Chạy
                process = subprocess.Popen(command, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE, cwd=testdir)
                process_stdout, process_stderr = process.communicate()
                process_stdout = process_stdout.decode('utf-8')
                process_stderr = process_stderr.decode('utf-8')
                exit_code = process.returncode

                # Fix output của checker
                process_stderr = process_stderr.strip('\r')
                process_stderr = process_stderr.strip('\n')
                checker_message = process_stderr
                if len(checker_message):
                    checker_message += '\n'
                checker_message += process_stdout

                if exit_code: # WRONG ANSWER ---------------------------------------------------------
                    submission_result.result = SubmissionResultType.WA
                    submission_result.checker_message = checker_message
                    submission_result.save()
                    scorer.onWrongAnswer()
                else: # ACCEPT ---------------------------------------------------------
                    submission_result.points = testcase.points
                    submission_result.checker_message = checker_message
                    submission_result.result = SubmissionResultType.AC
                    submission_result.save()
                    scorer.onAccept(testcase.points)
                    sumMemoryUsage += memory_usage
                    sumExecuteTime += execute_time
                    numberOfAC += 1
            else:
                if result == SubmissionResultType.TLE: # TIME LIMIT ---------------------------------------------------------
                    submission_result.executed_time = max(execute_time, time_limit + 1)
                    submission_result.memory_usage = memory_usage
                    submission_result.result = SubmissionResultType.TLE
                    submission_result.save()
                    scorer.onTimeLimitExceeded()
                if result == SubmissionResultType.MLE: # MEMORY LIMIT ---------------------------------------------------------
                    submission_result.memory_usage = max(memory_usage, memory_limit + 1)
                    submission_result.result = SubmissionResultType.MLE
                    submission_result.save()
                    scorer.onMemoryLimitExceeded()
                if result == SubmissionResultType.RTE: # RUNTIME ERROR ---------------------------------------------------------
                    submission_result.result = SubmissionResultType.RTE
                    submission_result.save()
                    scorer.onRunTimeError()
                if result == SubmissionResultType.SYS_ERROR: # SYSTEM ERROR ---------------------------------------------------------
                    raise Exception('SYSTEM ERROR')

        submission.status = SubmissionStatusType.Completed
        submission.result = scorer.getSubmissionResult()
        submission.points = scorer.getTotalScore()

        if submission.result == SubmissionResultType.TLE:
            submission.executed_time = submission_result.executed_time
        else:
            submission.executed_time = sumExecuteTime // numberOfAC if numberOfAC else 0
        
        if submission.result == SubmissionResultType.MLE:
            submission.memory_usage = submission_result.memory_usage
        else:
            submission.memory_usage = sumMemoryUsage // numberOfAC if numberOfAC else 0
        
        submission.save()
        return (status, result, 0, 0, '')

