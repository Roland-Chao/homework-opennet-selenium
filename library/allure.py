import os
import allure
import uuid
from functools import wraps
from library.logger import HandleLog

def conditional_allure_attach_log(condition=True, log_name=None):
    def decorator(func):
        if not condition:
            return func
        
        original_func = func.__get__(None, object) if isinstance(func, staticmethod) else func
        
        @wraps(original_func)
        def wrapper(*args, **kwargs):
            unique_id = str(uuid.uuid4())[:4]
            log_filename = f"{log_name or original_func.__name__}_{unique_id}.txt"
            log = HandleLog()
            try:
                log.add_file_handler(log_filename)

                step_name = log_name or original_func.__name__
                with allure.step(f"{step_name}"):
                    log.info_log(f"----- {step_name} -----")
                    return original_func(*args, **kwargs)

            finally:
                log.remove_file_handler(log_filename)
                if os.path.exists(log_filename):
                    with open(log_filename, "r") as f:
                        allure.attach(f.read(), name=log_filename, attachment_type=allure.attachment_type.TEXT)
                    os.remove(log_filename)
        
        if isinstance(func, staticmethod):
            return staticmethod(wrapper)
        return wrapper
    return decorator

def allure_attach_log(log_name=None):
    return conditional_allure_attach_log(condition=True, log_name=log_name)