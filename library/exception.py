# ================= Page Utils Exception =================
class PageUtilsException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

class PageUtilsTimeoutException(PageUtilsException):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

class PageUtilsElementException(PageUtilsException):
    def __init__(self, message):
        super().__init__(message)
        self.message = message
class PageUtilsOtherException(PageUtilsException):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

class CustomException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

# ================= API Utils Exception =================
class InvalidResponseError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

class StatusCheckError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

class AssertError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

class SendRequestError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

class API504Error(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

class API503Error(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

class API500Error(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

class API404Error(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

class API403Error(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

class API400Error(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

class APIOtherStatusCodeError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

class CompareDataError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message