from pybaseballdatana.analysis.simulations import PlayerRegistry, Batter, Lineup


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
