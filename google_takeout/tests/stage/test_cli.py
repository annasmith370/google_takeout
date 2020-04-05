
import pytest
from click.testing import CliRunner
from google_takeout.stage import cli

@pytest.mark.parametrize(
    "name,expected_output",
    [
        ["myProduct", "my-product"],
        ["MyProduct", "my-product"],
        ["myProductTwo", "my-product-two"],
        ["MYProductTwo", "my-product-two"],
    ]
)
def test_product_command_name(name: str, expected_output: str):
    assert cli.product_command_name(name) == expected_output

def test_get_all_products():
    class FakeProductOne: pass
    class FakeProductTwo: pass
    class FakeProductThree: pass
    PRODUCTS = {FakeProductOne, FakeProductTwo, FakeProductThree}

    assert cli.get_all_products(PRODUCTS) == {
        "fake-product-one": FakeProductOne,
        "fake-product-two": FakeProductTwo,
        "fake-product-three": FakeProductThree
    }
