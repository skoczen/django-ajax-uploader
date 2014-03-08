from django.dispatch import Signal


file_uploaded = Signal(providing_args=['backend', 'request'])
