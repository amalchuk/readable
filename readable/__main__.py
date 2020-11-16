import os
import os.path
import sys
from typing import List

from django.core.management import ManagementUtility as BaseManagementUtility

# Add parent-parent directory:
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Default settings:
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "readable.settings.development")


class ManagementUtility(BaseManagementUtility):
    def __init__(self) -> None:
        arguments: List[str] = sys.argv.copy()
        executable = arguments[0] = " ".join(["python", "-m", "readable"])
        super(ManagementUtility, self).__init__(arguments)
        self.prog_name = executable


def execute_from_command_line() -> None:
    utility = ManagementUtility()
    utility.execute()


if __name__ == "__main__":  # pragma: no cover
    execute_from_command_line()
