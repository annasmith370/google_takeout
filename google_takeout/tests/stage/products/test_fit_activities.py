
from collections import defaultdict
from google_takeout.stage.products.fit import activities

TEXT_VALUES = {"found1", "not_found1"}
ATTRIBUTE_VALUES = {"found2", "not_found2"}


class MockRoot:
    attrib = {"found2": "foo", "not_asked_for": "bar"}

    def find(self, looking_for, namespace):
        looking_for = looking_for.replace("Activities:", "")
        assert looking_for in TEXT_VALUES
        assert namespace == activities.NAMESPACE

        if looking_for == "found1":

            class MockSubRoot:
                text = "foo"

            return MockSubRoot()
        elif looking_for == "not_found1":
            return None
        else:
            raise ValueError(f"unexpected {looking_for}")


def test_get_text_values():
    assert activities.FitActivities().get_text_values(MockRoot(), TEXT_VALUES) == {
        "found1": "foo",
        "not_found1": None,
    }


def test_get_attrib_values():
    assert activities.FitActivities().get_attrib_values(
        MockRoot(), ATTRIBUTE_VALUES
    ) == {"found2": "foo", "not_found2": None,}


def test_empty_root_dict():

    data = "place holder - this should be returned immediately"
    assert activities.FitActivities().add_root_dict(data, None, None) == data


def test_add_root_dict():
    mock_xml = {
        "table_baz": {
            "texts": ["found1", "not_found1"],
            "attributes": ["found2", "not_found2"],
        },
    }

    data = {
        "table_baz": [ 
            "This data already existed"
        ]
    }
    res = activities.FitActivities().add_root_dict(
        data, 
        MockRoot(), 
        "table_baz", 
        mock_xml, 
        extra1="Extra!", 
        extra2="Some more!"
    )
    assert res == {
        "table_baz": [
            "This data already existed",
            {
                "found1": "foo", 
                "not_found1": None, 
                "found2": "foo", 
                "not_found2": None, 
                "extra1": "Extra!", 
                "extra2": "Some more!"
            }
        ]
    }

    