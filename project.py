import csv

def main():
    players = load_data("nba_data.csv")
    minimum_minutes = 1000
    while True:
        print("\n===============================================")
        print(" NBA Salary Efficiency Analyzer")
        print("===============================================")
        print(f"Current Minimum Minutes: {minimum_minutes}")
        print("-----------------------------------------------")
        print("1. View Top Players")
        print("2. Search Player")
        print("3. Compare Players")
        print("4. Change Minimum Minutes")
        print("5. Exit")

        choice = input("Choice: ")

        if choice == "1":
            filtered = filter_players(players, minimum_minutes)
            try:
                amount = int(input("How many players would you like listed?: "))
                if amount <= 0:
                    print("Please enter a positive number")
                    input("\nPress enter to return to menu...")
                    continue
            except ValueError:
                print("Please enter a valid number")
                input("\nPress enter to return to menu...")
                continue
            display_top_players(filtered, amount)
            input("\nPress enter to return to menu...")
        elif choice == "2":
            name = input("Player Name: ")
            player = find_player(players, name)
            if player:
                print("\n===============================================")
                print(f"{player['Player']} ({player['Team']})")
                print("================================================")
                print(display_player(player))
            else:
                print("Player Not Found")
            input("\nPress enter to return to menu...")
        elif choice == "3":
            first_name = input("First Player: ")
            second_name = input("Second Player: ")
            player1 = find_player(players, first_name)
            player2 = find_player(players, second_name)
            if not player1 or not player2:
                print("Player Not Found")
            else:
                print("\n===============================================")
                print("Player Comparison")
                print("================================================")
                print(compare_players(player1, player2))
                print("-----------------------------------------------")
                input("\nPress enter to return to menu...")
        elif choice == "4":
            try:
                new_minimum = int(input("What are the minimum minutes for players to qualify?: "))

                if new_minimum < 0:
                    print("Please enter 0 or a positive number.")
                else:
                    minimum_minutes = new_minimum
                    print(f"Minimum minutes set to {minimum_minutes}.")
            except ValueError:
                print("Please enter a valid number.")
            input("\nPress enter to return to menu...")
        elif choice == "5":
            print("\nThank you for using my NBA Salary Efficiency Analyzer!")
            break
        else:
            print("Invalid Choice")


def load_data(filename):
    data = []

    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row["Salary"] = int(row["Salary"].replace("$", "").replace(",", ""))
            row["Minutes"] = int(row["Minutes"])
            row["Points"] = int(row["Points"])
            row["Rebounds"] = int(row["Rebounds"])
            row["Assists"] = int(row["Assists"])
            data.append(row)
        return data


def calculate_production(player):
    production = player["Points"] + player["Rebounds"] * 1.2 + player["Assists"] * 1.5
    return production


def calculate_efficiency(player):
    production = calculate_production(player)
    efficiency = production / (player["Salary"] / 1000000)
    return round(efficiency, 2)


def add_efficiency(players):
    for player in players:
        player["Efficiency"] = calculate_efficiency(player)
    return players


def rank_players(players):
    players = add_efficiency(players)
    players.sort(key=lambda player: player["Efficiency"], reverse=True)
    return players


def filter_players(players, minimum_minutes):
    filtered = []

    for player in players:
        if player["Minutes"] >= minimum_minutes:
            filtered.append(player)
    return filtered


def find_player(players, name):
    for player in players:
        if player["Player"].lower() == name.lower():
            return player
    return None


def display_top_players(players, amount):
    ranked = rank_players(players)

    print("\n================ Top Players ================")

    for number, player in enumerate(ranked[:amount], start=1):
        print(f"{number}. {player['Player']} ({player['Team']})")
        print(f"Efficiency: {player['Efficiency']:.2f}")
        print()


def display_player(player):
    if player:
        return f"Salary: ${player['Salary']:,}\nMinutes: {player['Minutes']:,}\n\nPoints: {player['Points']}\nRebounds: {player['Rebounds']}\nAssists: {player['Assists']}\n\nProduction: {calculate_production(player):,.1f}\nEfficiency: {calculate_efficiency(player):.2f}"


def compare_players(player1, player2):
    efficiency1 = calculate_efficiency(player1)
    efficiency2 = calculate_efficiency(player2)

    if efficiency1 > efficiency2:
        winner = player1
    else:
        winner = player2

    efficiency_difference = abs(efficiency1 - efficiency2)
    return f"{player1['Player']} ({player1['Team']})\nSalary: ${player1['Salary']:,}\nProduction: {calculate_production(player1):,.1f}\nEfficiency: {calculate_efficiency(player1):.2f}\n\n{player2['Player']} ({player2['Team']})\nSalary: ${player2['Salary']:,}\nProduction: {calculate_production(player2):,.1f}\nEfficiency: {calculate_efficiency(player2):.2f}\n-----------------------------------------------\nBetter Value: {winner['Player']}\n\nEfficiency Difference: {efficiency_difference:.2f}"


if __name__ == "__main__": main()
