from pybaseballdatana.analysis.simulations import Batter, Lineup


def test_lineup():
    batter = Batter(player_id="abc123")
    batter.set_batting_event_probs(
        base_on_balls=0.08, single=0.15, double=0.05, triple=0.006, home_run=0.03
    )
    lineup = Lineup(lineup=[batter] * 9)

    other_batter = Batter(player_id="xyz789")
    batter.set_batting_event_probs(
        base_on_balls=0.18, single=0.15, double=0.05, triple=0.006, home_run=0.03
    )
    lineup.set_lineup_slot(1, other_batter)
