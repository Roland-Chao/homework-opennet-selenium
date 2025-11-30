import allure
import pytest
import requests
import os
from pathlib import Path
from api_object.the_dog_api import TheDogAPI
from library.validator import Validator
from conftest import load_test_data

@pytest.mark.API
@allure.parent_suite("The Dog API")
@allure.suite("Favourites API")
class TestDogAPIFavourites:
    DATA_DIR = Path(__file__).parent / "case_data"
    validator = Validator()

    @allure.sub_suite("Favourite Success Test")
    @pytest.mark.TheDogAPI
    @pytest.mark.parametrize(
        "test_case",
        load_test_data(str(DATA_DIR / "favourite_success")),
        ids=lambda x: x["test_id"]
    )
    def test_favourite_success(self, test_case):
        session = requests.Session()
        dog_api = TheDogAPI(session, api_key=os.getenv('DOG_API_KEY'))

        with allure.step(f"Add favourite with valid data"):
            dog_api.add_favourite(json=test_case["payload"])\
                .check_status_success()

        response_data = dog_api.get_response_data()

        with allure.step("Verify success response"):
            self.validator.assert_is_equal(
                expected=test_case["expected_data"]["message"],
                actual=response_data.get("message")
            )

            self.validator.assert_greater(
                actual=response_data.get("id"),
                expected=0,
                key="Id"
            )

    @allure.sub_suite("Favourite Error Test")
    @pytest.mark.TheDogAPI
    @pytest.mark.parametrize(
        "test_case",
        load_test_data(str(DATA_DIR / "favourite_error")),
        ids=lambda x: x["test_id"]
    )
    def test_favourite_error(self, test_case):
        session = requests.Session()

        # Handle API key scenarios
        if test_case.get("use_api_key") == False:
            api_key = None
        else:
            api_key = os.getenv('DOG_API_KEY')

        dog_api = TheDogAPI(session, api_key=api_key)

        with allure.step(f"Attempt to add favourite with invalid data"):
            dog_api.add_favourite(json=test_case["payload"])\
                .check_status_error(expected_error_code=test_case["expected_status_code"])

            response_text = dog_api.response.text
            self.validator.assert_in(
                expected=test_case["expected_error"],
                actual=response_text,
                key="Error Text"
            )
