import csv

# Knapsack function
def knapsack(weights, values, capacity):
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            if weights[i-1] <= w:
                dp[i][w] = max(dp[i-1][w], dp[i-1][w-weights[i-1]] + values[i-1])
            else:
                dp[i][w] = dp[i-1][w]

    selected_items = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i-1][w]:
            selected_items.append(i-1)
            w -= weights[i-1]
    
    return dp[n][capacity], selected_items

# Load player data from the CSV file
file_path = "/Users/jeremycarter/Code/FantasyFootball/2023-24 Fantasy Football - Copy of PPAD.csv"
players = {}
with open(file_path, mode='r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        position = row["Position"]
        name = row["Player"]
        value = float(row["Value"])
        cost = row["Cost"]

        if not cost or cost.lower() == 'null' or cost.strip() == "":
            continue

        cost = int(float(cost.replace("$", "").strip()) * 100)

        if position not in players:
            players[position] = []
        players[position].append({"name": name, "value": value, "cost": cost})

# Budget allocation
total_budget = 20000  # $200 * 100
allocated_budgets = {
    "QB": int(total_budget * 0.15),
    "RB": int(total_budget * 0.25),
    "WR": int(total_budget * 0.25),
    "TE": int(total_budget * 0.10),
    "Flex": int(total_budget * 0.10),
    "Superflex": int(total_budget * 0.05),
    "Def": int(total_budget * 0.05),
    "Bench": int(total_budget * 0.05)
}

team = {}
for position, number in desired_team_structure.items():
    if position not in players:
        continue

    pos_players = players[position]
    values = [player["value"] for player in pos_players]
    costs = [player["cost"] for player in pos_players]

    current_budget = int(allocated_budgets[position])

    max_value, selected = knapsack(costs, values, current_budget)
    team[position] = [pos_players[i]["name"] for i in selected]

    # Deduct the spent budget
    allocated_budgets[position] -= sum(pos_players[i]["cost"] for i in selected)

    # Remove selected players so they're not considered again
    for i in selected:
        players[position].remove(pos_players[i])

print(team)
