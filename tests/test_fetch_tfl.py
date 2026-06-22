import json

from fetch_tfl import save_tfl_data, print_line_statuses

# no need to call TfL API - create fake data
FAKE_DATA = [
    {
        "name": "Waterloo & City",
        "lineStatuses": [{"statusSeverityDescription": "Minor Delays"}],
    }
]


def test_save_tfl_data(tmp_path):
    # create temp file path
    saved_file_path = save_tfl_data(FAKE_DATA, output_dir=tmp_path)

    # open path and check if the saved data is the same as the fake data
    with open(saved_file_path) as file:
        saved_data = json.load(file)

    assert FAKE_DATA == saved_data


# capsys and tmp_path come from pytest itself (as fixtures)
def test_print_line_statuses(capsys):
    print_line_statuses(FAKE_DATA)
    captured = capsys.readouterr()

    assert captured.out == "Waterloo & City : Minor Delays\n"
