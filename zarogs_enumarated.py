import json

with open('cards.json', encoding="utf8") as json_file:
    data = json.load(json_file)
    print(data[0].keys())
    bad_keys = ['artist', 'collectible', 'flavor', 'dbfId', 'elite', 'id', 'playRequirements']
    for i in range(len(data)):
        for key in bad_keys:
            try:
                data[i].pop(key)
            except:
                pass

def stats(card):
    return card['attack'] + card['health']
def main():
    player_class = 'ROGUE'
    leg_minion = []
    for card in data:
        if card['rarity'] == 'LEGENDARY' and card['type'] == 'MINION':
            if card['cardClass'] == 'NEUTRAL':
                leg_minion.append(card)
            if card['cardClass'] == player_class:
                for i in range(4):#class discovery bonus
                    leg_minion.append(card)

    print(len(leg_minion), 'legendaries in wild')
    std_leg = []
    std = ['BOOMSDAY', 'CORE', 'EXPERT1', 'TROLL', 'GILNEAS', 'DALARAN']
    counters = {}
    for card in leg_minion:
        if card['set'] in std:
            std_leg.append(card)
            try:
                counters[card['set']] += 1
            except:
                counters[card['set']] = 1
    print(counters)
    print(len(std_leg), 'legendaries in standard')
    combinations = []
    for i in range(len(std_leg)):
        for j in range(len(std_leg)):
            if j == i:
                continue
            for k in range(len(std_leg)):
                if k == j or k == i:
                    continue
                # combinations need to represent different weighting towards class legendaries
                # however, you can't have multiple of same card
                if std_leg[i] != std_leg[j] and std_leg[i] != std_leg[k] and std_leg[j] != std_leg[k]:
                    combinations.append((std_leg[i], std_leg[j], std_leg[k]))
    n = len(combinations)
    print(n, "combinations")
    c = 0

    #pick highest average
    pick_max = 0
    a,h = 0,0
    total_a = 0
    total_h = 0
    for discovery in combinations:
        max = 0
        for card in discovery:
            if stats(card) > max:
                max = stats(card)
                a = card['attack']
                h = card['health']
        pick_max += max
        total_a += a
        total_h += h

    print(pick_max/n)
    print(total_a/n)
    print(total_h/n)

    #pick highest attack
    pick_max = 0
    a, h = 0, 0
    total_a = 0
    total_h = 0
    for discovery in combinations:
        max = 0
        for card in discovery:
            if card['attack'] > max:
                max = stats(card)
                a = card['attack']
                h = card['health']
        pick_max += max
        total_a += a
        total_h += h

    print(pick_max / n)
    print(total_a / n)
    print(total_h / n)

    # pick highest health
    pick_max = 0
    a, h = 0, 0
    total_a = 0
    total_h = 0
    for discovery in combinations:
        max = 0
        for card in discovery:
            if card['health'] > max:
                max = stats(card)
                a = card['attack']
                h = card['health']
        pick_max += max
        total_a += a
        total_h += h

    print(pick_max / n)
    print(total_a / n)
    print(total_h / n)


if __name__ == '__main__':
    main()