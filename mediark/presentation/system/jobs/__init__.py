from .send_email import SendEmailJob

JOBS = [value for key, value in globals().items() if key.endswith('Job')]
