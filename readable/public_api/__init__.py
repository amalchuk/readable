# Copyright 2020-2021 Andrew Malchuk. All rights reserved.
# This project is licensed under the terms of the MIT License.

"""
Public REST API.
"""

from typing import Final

__all__: Final[list[str]] = ["default_app_config"]

default_app_config: str = "readable.public_api.apps.Configuration"
