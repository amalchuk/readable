# Copyright 2020 Andrew Malchuk. All rights reserved.
# This project is licensed under the terms of the MIT License.

"""
Check and improve the spelling and grammar of documents.
"""

from readable.crontab import application as celery

__all__ = ("celery", "default_app_config")

default_app_config = "readable.apps.Configuration"
