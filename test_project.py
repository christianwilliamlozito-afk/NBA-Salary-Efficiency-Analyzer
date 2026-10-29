from project import (calculate_production, calculate_efficiency, filter_players, find_player)

def test_calculate_production():
    player = {"Points": 20, "Rebounds": 10, "Assists": 5,}
    assert calculate_production(player) == 39.5


def test_calculate_efficiency():
    player = {"Points": 20, "Rebounds": 10, "Assists": 5, "Salary": 1_000_000,}
    assert calculate_efficiency(player) == 39.5


def test_filter_players():
    players = [
        {"Player": "Player A", "Minutes": 1500},
        {"Player": "Player B", "Minutes": 800},
        {"Player": "Player C", "Minutes": 1000},
    ]

    filtered = filter_players(players, 1000)

    assert len(filtered) == 2
    assert filtered[0]["Player"] == "Player A"
    assert filtered[1]["Player"] == "Player C"

def test_find_players():
    players = [
        {"Player": "Lebron James"},
        {"Player": "Stephen Curry"},
    ]

    assert find_player(players, "Lebron James") == players[0]
    assert find_player(players, "lebron james") == players[0]
    assert find_player(players, "Jayson Tatum") is None

