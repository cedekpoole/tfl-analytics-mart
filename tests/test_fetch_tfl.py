import json

from fetch_tfl import save_tfl_data


def test_save_tfl_data(tmp_path):
    # no need to call TfL API - create fake data
    FAKE_DATA = [
        {
            "name": "Waterloo & City",
            "lineStatuses": [{"StatusSeverityDescription": "Minor Delays"}],
        }
    ]
    # create temp file path
    saved_file_path = save_tfl_data(FAKE_DATA, output_dir=tmp_path)

    # open path and check if the saved data is the same as the fake data
    with open(saved_file_path) as file:
        saved_data = json.load(file)

    assert FAKE_DATA == saved_data
