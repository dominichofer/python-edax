import platform
import subprocess
import tempfile
from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool
from typing import Iterable
from pathlib import Path
from .helpers import split, flatten
from .output import Line, Output


def _executable() -> Path:
    "Returns the path to the Edax executable."
    path = Path(__file__).parent / "bin"
    if not path.exists():
        raise FileNotFoundError("Edax binary not found.")
    if platform.system() == "Windows":
        return path / "edax-4.4-ms-windows"
    elif platform.system() == "Linux":
        return path / "edax-4.4-linux"
    else:
        raise OSError("Unsupported operating system.")


class Edax:
    "Edax wrapper."

    def __init__(
        self,
        hash_table_size: int | None = None,
        tasks: int | None = None,
        level: int | None = None,
    ):
        """
        exe_path: Path to Edax executable.
        hash_table_size: Hash table size in number of bits.
        tasks: Search in parallel using n tasks.
        level: Search using limited depth.
        """
        self.exe = _executable()
        self.hash_table_size = hash_table_size
        self.tasks = tasks
        self.level = level

    @staticmethod
    def name() -> str:
        "Returns the name of the engine."
        result = subprocess.run(
            [_executable(), "-v", "-h"], capture_output=True, check=True, text=True
        )
        return " ".join(result.stderr.split()[0:3])

    def _command(self, temp_file: str) -> list[str]:
        cmd = [str(self.exe), "-solve", temp_file]
        if self.hash_table_size is not None:
            cmd += ["-h", str(self.hash_table_size)]
        if self.tasks is not None:
            cmd += ["-n", str(self.tasks)]
        if self.level is not None:
            cmd += ["-l", str(self.level)]
        return cmd

    def solve(self, position: str | Iterable[str]) -> Output:
        "Solves positions."
        if isinstance(position, str):
            position = [position]
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write("\n".join(position).encode())
        result = subprocess.run(
            self._command(temp_file.name),
            cwd=self.exe.parent,
            capture_output=True,
            check=True,
            text=True,
        )
        return Output(result.stdout)


class MultiprocessEdax:
    "Edax wrapper using multiprocessing."

    def __init__(
        self,
        hash_table_size: int | None = None,
        tasks: int | None = None,
        level: int | None = None,
    ):
        self.edax = Edax(hash_table_size, tasks, level)

    @staticmethod
    def name() -> str:
        return Edax.name()

    def solve(self, position: str | Iterable[str]) -> list[Line]:
        if isinstance(position, str):
            position = [position]
        with ThreadPool() as pool:
            return flatten(
                pool.map(
                    lambda x: self.edax.solve(x).lines,
                    split(position, cpu_count()),
                )
            )
