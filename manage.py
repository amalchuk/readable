#!/usr/bin/env python

from os import environ

if __name__ == "__main__":
    environ.setdefault("DJANGO_SETTINGS_MODULE", "readable.settings.development")

    from django.core.management import execute_from_command_line
    execute_from_command_line()
