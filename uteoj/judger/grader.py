from abc import abstractclassmethod, ABC, abstractmethod
import subprocess
import os
from genericpath import exists
from posixpath import commonpath
from re import sub
from typing import Tuple, overload
from subprocess import check_output

from django.utils import timezone
from django.db import transaction

from backend.models.submission import SubmissionResultType, SubmissionStatusType, SubmissionModel, SubmissionTestcaseResultModel
from backend.models.usersetting import UserProblemStatisticsModel
from backend.models.problem import ProblemStatisticsModel, ProblemType

from judger.score import ACMScore, OIScore
from judger.graderabstract import GraderAbstract


class CppGrader(GraderAbstract):

    _name = 'C++ 14'
    _extension = '.cpp'
    _compiler_command = '/usr/bin/g++ -std=c++14     -O2   -Wall -fstack-protector-all   $SOURCE_NAME_EXT$   -o   $SOURCE_NAME$.out'
    _run_command = '$SOURCE_NAME$.out'
    _execute_name = '$SOURCE_NAME$.out'
    _description = 'Ngôn ngữ c++ 14'

    def __init__(self, compiler_workdir, run_workdir) -> None:
        super().__init__(compiler_workdir, run_workdir)


class JavaGrader(GraderAbstract):

    _name = 'Java 1.8'
    _extension = '.java'
    _compiler_command = '/usr/bin/javac $SOURCE_NAME_EXT$'
    _run_command = '/usr/bin/java -XX:MaxRAM=128M -DONLINE_JUDGE=true -Duser.language=en -Duser.region=US -Duser.variant=US $SOURCE_NAME$'
    _execute_name = '$SOURCE_NAME$.class'
    _description = 'Ngôn ngữ java 1.8'

    def __init__(self, compiler_workdir, run_workdir) -> None:
        super().__init__(compiler_workdir, run_workdir)

    def _prepare(self, source_code):
        open(os.path.join(self._compiler_workdir, 'Main.java'), 'w', encoding='utf-8').write(source_code)
        self._source_file_name = 'Main.java'

class PythonGrader(GraderAbstract):

    _name = 'Python 3.9'
    _extension = '.py'
    _compiler_command = '' # Không compile
    _run_command = '/usr/bin/python3     $SOURCE_NAME_EXT$'
    _execute_name = '$SOURCE_NAME_EXT$'
    _description = 'Ngôn ngữ python 3.9'

    def __init__(self, compiler_workdir, run_workdir) -> None:
        super().__init__(compiler_workdir, run_workdir)

    def _compileSource(self):
        # Không compile
        return (SubmissionStatusType.Grading, None, '')


source_cpp_test = """#include <bits/stdc++.h>

using namespace std;

int main() {
    //freopen("sumab.inp", "r", stdin);
    freopen("sumab.out", "w", stdout);
    int a, b;
    cin >> a >> b;
    if (a == 584) {
        while (a > 0) {
            a = a + 1;//forever
        }
    }
    else if (a == 408) {
        for (int i = 0; i < 1000; ++i) {
            int* tmp = new int[10000];
            for (int j = 1; j < 10000; ++j) {
                tmp[j] += tmp[j - 1];
            }
            //delete[] tmp;
        }
    }
    else if (a == 456) {
        char* mem = (char*)0xb8000;
        for (int i = 0; i < 1000; ++i) {
            mem[2 * i] = 'A';
            mem[2 * i + 1] = 0x07;
        }
        //return 162;
    }
    else if (a == 301) {
        char* str;
        str = "Hello World";
        *(str + 7) = 'Z';
    }
    else if (a == 405) {
        return 12;
    }
    else if (a == 432 || a == 173) a++;
    cout << a + b;
    cerr << "STDERRRRR HERE!!!";
    return 0;
}
"""

def compileChecker(problem):
    result, msg = GraderAbstract.compileChecker(problem)
    if result == False:
        print('Biên dịch checker lỗi!')
        print(msg)
        exit(0)
    else:
        print('Checker ok')

def cppTest(com, run, problem):
    grader = CppGrader(com, run)
    status, result, execute_time, memory_usage, msg = grader.grading(
        source_cpp_test,
        problem,
        'sumab.inp',
        'sumab.out',
        1000,
        1024 * 39,
        True,
        False,
        True,
        ProblemType.ACM)
    if result == SubmissionResultType.CE:
        print('Dịch lỗi')
        print(msg)
    else:
        pass

COMPILER_WORKING_DIR = 'compiler/123'
RUN_WORKING_DIR = 'run/456'
PROBLEM_DIR = 'problem/sumab/'
