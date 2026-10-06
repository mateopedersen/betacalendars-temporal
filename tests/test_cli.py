import json

from betacalendars.cli import main


def test_month_markdown_cli(capsys) -> None:
    assert main(["month", "2027", "1"]) == 0
    assert "## January 2027" in capsys.readouterr().out


def test_json_year_and_range_cli(capsys) -> None:
    assert main(["year", "2027", "--format", "json"]) == 0
    assert len(json.loads(capsys.readouterr().out)["months"]) == 12
    assert main(["range", "2026-12-31", "2027-01-01", "--format", "json"]) == 0
    assert len(json.loads(capsys.readouterr().out)["dates"]) == 2


def test_invalid_month_has_nonzero_status(capsys) -> None:
    assert main(["month", "2027", "13"]) == 2
    assert "month must be an integer" in capsys.readouterr().err
