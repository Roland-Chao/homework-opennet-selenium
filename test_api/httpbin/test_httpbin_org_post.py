import allure
import pytest
import requests
from pathlib import Path
from api_object.httpbin_org import HttpbinOrg
from library.validator import Validator
from conftest import load_test_data

@pytest.mark.API
@allure.parent_suite("HttpBinOrg API")
@allure.suite("POST API")
class TestHttpBinOrgPost:
    DATA_DIR = Path(__file__).parent / "case_data"
    validator = Validator()

    @allure.sub_suite("Response Verify Success Test")
    @pytest.mark.HttpBinOrg
    @pytest.mark.parametrize(
        "test_case",
        load_test_data(str(DATA_DIR / "verify_success")),
        ids=lambda x: x["test_id"]
    )
    def test_verify_success(self, test_case):
        session = requests.Session()
        httpbin_org = HttpbinOrg(session)
        response_data = httpbin_org.post(json=test_case["payload"])\
            .check_status_success()\
            .get_response_data("json")

        self.validator.deep_diff_compare(
            actual_data=response_data,
            expected_data=test_case["expected_data"]
        )
    
    @allure.sub_suite("ResponseVerify Error Test")
    @pytest.mark.HttpBinOrg
    @pytest.mark.parametrize(
        "test_case",
        load_test_data(str(DATA_DIR / "verify_error")),
        ids=lambda x: x["test_id"]
    )
    def test_verify_error(self, test_case):
        session = requests.Session()
        httpbin_org = HttpbinOrg(session)

        response_data = httpbin_org.post(json=test_case["payload"])\
            .check_status_success()\
            .get_response_data("json")

        self.validator.deep_diff_compare(
            actual_data=response_data,
            expected_data=test_case["expected_data"]
        )