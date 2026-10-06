from betacalendars import year_grid


def test_year_grid_has_twelve_ordered_months() -> None:
    grid = year_grid(2027, fixed_rows=True)
    assert len(grid.months) == 12
    assert [month.month for month in grid.months] == list(range(1, 13))
    assert all(len(month.cells) == 42 for month in grid.months)


def test_year_json_contains_all_months() -> None:
    import json

    value = json.loads(year_grid(2027).to_json())
    assert value["year"] == 2027
    assert len(value["months"]) == 12
