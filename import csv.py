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
with open('data.csv', mode='r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        position = row["Position"]
        name = row["Name"]
        value = int(row["Value"])
        cost = row["Cost"]

        # Handle 'null' or missing costs
        if not cost or cost.lower() == 'null':
            continue  # This excludes players with null costs. 

        cost = int(cost)
        
        if position not in players:
            players[position] = []
        players[position].append({"name": name, "value": value, "cost": cost})

# Budget allocation
total_budget = 100
starting_budget = total_budget * 0.95
bench_budget = total_budget * 0.05

# Define desired team structure
desired_team_structure = {
    "QB": 1,
    "RB": 2,
    "WR": 3,
    "TE": 1,
    "Flex": 1,
    "Superflex": 1,
    "Def": 1,
    "Bench": 6
}

# Best starting lineup construction
team = {}
for position, number in desired_team_structure.items():
    if position not in players:
        continue

    pos_players = players[position]
    values = [player["value"] for player in pos_players]
    costs = [player["cost"] for player in pos_players]

    # Check if we are filling bench spots
    if position == "Bench":
        current_budget = bench_budget
    else:
        current_budget = starting_budget

    max_value, selected = knapsack(costs, values, current_budget)
    team[position] = [pos_players[i]["name"] for i in selected]

    # Deduct the spent budget
    if position == "Bench":
        bench_budget -= sum(pos_players[i]["cost"] for i in selected)
    else:
        starting_budget -= sum(pos_players[i]["cost"] for i in selected)

    # Remove selected players so they're not considered again
    for i in selected:
        players[position].remove(pos_players[i])

print(team)
