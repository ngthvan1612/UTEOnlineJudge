import os
from backend.models.submission import SubmissionStatusType
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


class CSharpGrader(GraderAbstract):

    _name = 'Mono C#'
    _extension = '.cs'
    _compiler_command = '/usr/bin/mcs   -out:$SOURCE_NAME$.exe   $SOURCE_NAME_EXT$' 
    _run_command = '/usr/bin/mono     $SOURCE_NAME$.exe'
    _execute_name = '$SOURCE_NAME$.exe' # error
    _description = 'Ngôn ngữ Mono C#'

    def __init__(self, compiler_workdir, run_workdir) -> None:
        super().__init__(compiler_workdir, run_workdir)

