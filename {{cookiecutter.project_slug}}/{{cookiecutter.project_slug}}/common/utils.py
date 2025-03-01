import os
import uuid
from functools import wraps
from typing import Callable

import requests
from django.conf import settings


def get_file_path(instance, filename: str) -> str:
    """Generate a UUID-based path for uploaded files.

    Example: uploads/2023/04/uuid4-filename.ext
    """
    ext = filename.split(".")[-1]
    filename = f"{uuid.uuid4()}-{filename}"
    return os.path.join("uploads", filename)


def check_recaptcha(view_func: Callable) -> Callable:
    """Decorator to validate reCAPTCHA response.

    Add to views that need CAPTCHA validation.
    """

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        request.recaptcha_is_valid = None
        if request.method == "POST":
            recaptcha_response = request.POST.get("g-recaptcha-response")
            data = {"secret": settings.RECAPTCHA_SECRET_KEY, "response": recaptcha_response}
            r = requests.post("https://www.google.com/recaptcha/api/siteverify", data=data)
            result = r.json()
            if result["success"]:
                request.recaptcha_is_valid = True
            else:
                request.recaptcha_is_valid = False
        return view_func(request, *args, **kwargs)

    return wrapper
