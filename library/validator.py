import allure, re, json
from library.logger import HandleLog
from library.allure import allure_attach_log
from deepdiff import DeepDiff
from library.exception import *

class Validator:
    host = '[Validator]'
    log = HandleLog()
    method = ","

    def _log_assert(self, assertion, expected, actual, key=None):
        key_info = f"[Key: {key}] " if key else ""
        match self.method:
            case "in" | "not in" | "in list":
                step_msg = f"Validate data {key_info} Expected: {expected} {self.method} Actual: {actual}"
                success_msg = f"{self.host} {key_info} Validation passed: Expected: {expected} {self.method} Actual: {actual}"
                fail_msg = f"{self.host} {key_info} Validation failed: Expected: {expected} {self.method} Actual: {actual}"
            case _:
                step_msg = f"Validate data {key_info} Actual: {actual} {self.method} Expected: {expected}"
                success_msg = f"{self.host} {key_info} Validation passed: Actual: {actual} {self.method} Expected: {expected}"
                fail_msg = f"{self.host} {key_info} Validation failed: Actual: {actual} {self.method} Expected: {expected}"

        with allure.step(step_msg):
            if assertion:
                self.log.info_log(success_msg)
            else:
                self.log.error_log(fail_msg)
                assert assertion, fail_msg

    def assert_is_equal(self, actual, expected, key=None) -> None:
        self.method = "="
        result = expected == actual
        self._log_assert(result, expected, actual, key)

    def assert_not_equal(self, actual, expected, key=None) -> None:
        self.method = "!="
        result = actual != expected
        self._log_assert(result, expected, actual, key)

    def assert_in(self, actual, expected, key=None) -> None:
        self.method = "in"
        result = expected in actual
        self._log_assert(result, expected, actual, key)

    def assert_in_list(self, actual, expected_list, key=None) -> None:
        self.method = "in list"
        if isinstance(actual, list):
            result = any(item in expected_list for item in actual)
        else:
            result = actual in expected_list
        self._log_assert(result, actual, expected_list, key)

    def assert_not_in(self, actual, expected, key=None) -> None:
        self.method = "not in"
        result = expected not in actual
        self._log_assert(result, expected, actual, key)

    def assert_greater(self, actual, expected, key=None) -> None:
        self.method = ">"
        result = actual > expected
        self._log_assert(result, expected, actual, key)

    def assert_greater_or_equal(self, actual, expected, key=None) -> bool:
        self.method = ">="
        result = actual >=  expected
        self._log_assert(result, expected, actual, key)

    def assert_less_than_or_equal(self, actual, expected, key=None) -> bool:
        self.method = "<="
        result = actual <= expected
        self._log_assert(result, expected, actual, key)

    def assert_less(self, actual, expected, key=None) -> None:
        self.method = "<"
        result = actual < expected
        self._log_assert(result, expected, actual, key)

    def assert_true(self, message, key=None):
        key_info = f"[Key: {key}] " if key else ""
        self.log.info_log(f"{self.host} {key_info}Validation passed: {message}")
        assert True

    def assert_false(self, message, key=None):
        key_info = f"[Key: {key}] " if key else ""
        self.log.error_log(f"{self.host} {key_info}Validation failed: {message}")
        assert False, f"{key_info}{message}"

    def assert_at_least(self, key, exp_value, act_value):
        self.log.info_log(f"{self.host} key: {key}, exp_value: {exp_value}, act_value: {act_value}")
        assert act_value >= exp_value, f"{self.host} Validation [{key}] act_value: {act_value} >= exp_value: {exp_value}"

    def assert_text_format(self, pattern, text, key=None):
        key_info = f"[Key: {key}] " if key else ""
        self.log.info_log(f"{self.host} {key_info} Validate text format: {text}")
        assert re.match(pattern, text), f"{self.host} {key_info} Expected format: {pattern}, but actual: {text}"

    @allure_attach_log(log_name="Deep diff compare")
    def deep_diff_compare(self, actual_data, expected_data, **kwargs):
        diff = DeepDiff(actual_data, expected_data, **kwargs)

        allure.attach(
            json.dumps(expected_data, indent=4, ensure_ascii=False),
            name="Expected data",
            attachment_type=allure.attachment_type.JSON
        )

        allure.attach(
            json.dumps(actual_data, indent=4, ensure_ascii=False),
            name="Actual data",
            attachment_type=allure.attachment_type.JSON
        )

        if diff:
            diff_message = json.dumps(diff, indent=4, ensure_ascii=False) if isinstance(diff, dict) else str(diff)
            error_msg = f"{self.host} Deep diff compare failed:\n{diff_message}"

            self.log.error_log(error_msg)

            allure.attach(
                diff_message,
                name="Diff Result",
                attachment_type=allure.attachment_type.TEXT
            )

            assert False, error_msg
        else:
            self.log.info_log(f"{self.host} Deep diff compare passed")
            assert True
