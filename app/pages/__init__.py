# app/pages/__init__.py
from .scanner import render_scanner_page
from .encyclopedia import render_encyclopedia_page
from .reports import render_reports_page
from .settings import render_settings_page

__all__ = [
    'render_scanner_page',
    'render_encyclopedia_page',
    'render_reports_page',
    'render_settings_page'
]