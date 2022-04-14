import re
from pybbda.analysis.simulations import PlayerRegistry, Batter


def test_player_regsitry_singleton():
    player_registry_one = PlayerRegistry()
    player_registry_two = PlayerRegistry()

    assert player_registry_one is player_registry_two


def test_player_registry_add():
    player_registry = PlayerRegistry()
    batter1 = Batter(player_id="abc")
    batter2 = Batter(player_id="xyz")

    player_registry.add([batter1, batter2])
    player_registry.add([batter1])
    player_registry.add(batter1)

    player_registry_too = PlayerRegistry()
    assert player_registry.len == player_registry_too.len


def test_from_lahman_records():
    player_registry = PlayerRegistry()
    lahman_records = player_registry._get_lahman_records(pa_limit=180)
    expected_columns = ("base_on_balls", "single", "double", "triple", "home_run")

    assert isinstance(lahman_records, dict)
    it = lahman_records.items().__iter__()
    key, record = next(it)
    assert all(column in record for column in expected_columns)
    assert len(record.values()) == len(expected_columns)
    assert re.match("[a-z]{,7}[0-9]{2}_[0-9]{4}", key)


def test_from_lahman():
    player_registry = PlayerRegistry()
    player_registry.load_from_lahman(pa_limit=180)
    assert player_registry.len > 30000
