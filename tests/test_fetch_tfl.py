import json
import pytest

from fetch_tfl import save_tfl_payload, print_line_statuses, validate_tfl_data

# no need to call TfL API - create fake data
FAKE_DATA = [
    {
        "name": "Waterloo & City",
        "lineStatuses": [{"statusSeverityDescription": "Minor Delays"}],
    }
]


def test_save_tfl_payload(tmp_path):
    # create temp file path
    saved_file_path = save_tfl_payload(FAKE_DATA, output_dir=tmp_path)

    # open path and check if the saved data is the same as the fake data
    with open(saved_file_path) as file:
        saved_data = json.load(file)

    assert FAKE_DATA == saved_data["data"]
    assert saved_data["source_url"] == "https://api.tfl.gov.uk/Line/Mode/tube/Status"
    assert "utc_fetched_at" in saved_data


# capsys and tmp_path come from pytest itself (as fixtures)
def test_print_line_statuses(capsys):
    print_line_statuses(FAKE_DATA)
    captured = capsys.readouterr()

    assert captured.out == "Waterloo & City : Minor Delays\n"


def test_validate_tfl_data():
    bad_data = [{"name": "Waterloo & City", "lineStatuses": [{}]}]

    with pytest.raises(ValueError):
        validate_tfl_data(bad_data)
