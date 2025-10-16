from .celery_app import app as celery_app

__all__ = ('celery_app',)

# Делается так, чтобы наш celery_app запускался вместе с Django
