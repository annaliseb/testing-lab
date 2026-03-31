import pytest
from leaderboard import Leaderboard


def test_add_player():
    lb = Leaderboard()
    lb.add_player("Alice")
    assert len(lb) == 1

def test_add_player_negative_score():
    lb = Leaderboard()
    with pytest.raises(ValueError, match="Initial score cannot be negative"):
        lb.add_player("Alice", -4)

def test_add_player_with_initial_score():
    lb = Leaderboard()
    lb.add_player("Alice", initial_score=500)
    assert lb.get_top_n(1) == [("Alice", 500)]

def test_add_player_duplicate():
    lb = Leaderboard()
    lb.add_player("Alice")
    with pytest.raises(ValueError, match="already registered"):
        lb.add_player("Alice")

def test_record_match_updates_scores():
    lb = Leaderboard()
    lb.add_player("Alice", 100)
    lb.add_player("Bob", 100)
    lb.record_match("Alice", "Bob")
    assert lb.get_top_n(2) == [("Alice", 110), ("Bob", 90)]

def test_record_match_not_registered_win():
    lb = Leaderboard()
    lb.add_player("Bob")
    with pytest.raises(KeyError, match="Player 'Alice' is not registered"):
        lb.record_match("Alice", "Bob")

def test_record_match_not_registered_lose():
    lb = Leaderboard()
    lb.add_player("Alice")
    with pytest.raises(KeyError, match="Player 'Bob' is not registered"):
        lb.record_match("Alice", "Bob")

def test_record_match_points_0():
    lb = Leaderboard()
    lb.add_player("Alice")
    lb.add_player("Bob")
    with pytest.raises(ValueError, match="Points must be positive"):
        lb.record_match("Alice", "Bob", 0)

def test_record_match_points_negative():
    lb = Leaderboard()
    lb.add_player("Alice")
    lb.add_player("Bob")
    with pytest.raises(ValueError, match="Points must be positive"):
        lb.record_match("Alice", "Bob", -10)

def test_get_rank():
    lb = Leaderboard()
    lb.add_player("Alice", 300)
    lb.add_player("Bob", 100)
    lb.add_player("Carol", 200)
    assert lb.get_rank("Alice") == 1
    assert lb.get_rank("Carol") == 2
    assert lb.get_rank("Bob") == 3

def test_get_rank_unregistered():
    lb = Leaderboard()
    with pytest.raises(KeyError, match="Player 'Alice' is not registered"):
        lb.get_rank("Alice")

def test_get_top_n_negative():
    lb = Leaderboard()
    with pytest.raises(ValueError, match="n must be non-negative"):
        lb.get_top_n(-1)

def test_get_top_n_zero():
    lb = Leaderboard()
    lb.add_player("Alice", 100)
    lb.add_player("Bob", 200)
    assert lb.get_top_n(0) == []

def test_get_percentile_single():
    lb = Leaderboard()
    lb.add_player("Alice", 100)
    assert lb.get_percentile("Alice") == 100.0

def test_get_percentile_unregistered():
    lb = Leaderboard()
    with pytest.raises(KeyError, match="Player 'Alice' is not registered"):
        lb.get_percentile("Alice")

def test_get_percentile():
    lb = Leaderboard()
    lb.add_player("Alice", 500)
    lb.add_player("Bob", 700)
    lb.add_player("Carol", 600)
    assert lb.get_percentile("Bob") == 66.67

def test_apply_bonus_unregistered():
    lb = Leaderboard()
    with pytest.raises(KeyError, match="Player 'Alice' is not registered"):
        lb.apply_bonus("Alice", 2)

def test_apply_bonus_updates_score():
    lb = Leaderboard()
    lb.add_player("Alice", 100)
    lb.apply_bonus("Alice", 2)
    assert lb.get_top_n(1) == [("Alice", 200)]

def test_reset():
    lb = Leaderboard()
    lb.add_player("Alice", 100)
    lb.add_player("Bob", 200)

    lb.reset()

    assert len(lb) == 0