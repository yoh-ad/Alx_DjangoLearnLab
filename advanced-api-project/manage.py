#!/usr/bin/env python
import os, sys
if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'advanced_api_project.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError('Django not installed. Run pip install -r requirements.txt') from exc
    execute_from_command_line(sys.argv)
