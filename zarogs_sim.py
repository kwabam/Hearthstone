import json
import random as rand
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde as kde
from matplotlib.colors import Normalize
from matplotlib import cm

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


def print_json_list(l):
    for card in l:
        print(json.dumps(card, indent=4))


def rarity_to_int(s1):
    if s1 == 'COMMON':
        s1 = 1
    elif s1 == 'RARE':
        s1 = 2
    elif s1 == 'EPIC':
        s1 = 3
    elif s1 == 'LEGENDARY':
        s1 = 4
    return s1


def compare_rarity(s1, s2):
    s1 = rarity_to_int(s1)
    s2 = rarity_to_int(s2)
    return s1 >= s2


# only does minions for now
def filter(cards=data, attack=0, health=0, rarity='', set='', type=''):
    filtered_cards = []
    print("filtering ", len(cards), "cards")
    for c in cards:
        if c['type'] == 'MINION':
            print(json.dumps(c))
            if c['attack'] >= attack and c['health'] >= health:
                if rarity == '' or compare_rarity(c['rarity'], rarity):
                    if set == '' or c['set'] == set:
                        filtered_cards.append(c)

    return filtered_cards

def zarogs_round(cards=data):
    discovered = []
    card = cards[rand.randint(0, len(cards) - 1)]
    for i in range(3):
        while card in discovered:
            card = cards[rand.randint(0, len(cards) - 1)]
        discovered.append(card)
    return discovered

def main():
    rogue = True
    leg_minion = []
    errors = 0
    for card in data:
        if card['rarity'] == 'LEGENDARY' and card['type'] == 'MINION':
            if card['cardClass'] == 'NEUTRAL':
                leg_minion.append(card)
            if rogue and card['cardClass'] == 'ROGUE':
                    leg_minion.append(card)
                    leg_minion.append(card)
                    leg_minion.append(card)
                    leg_minion.append(card)
                    #print(json.dumps(card, indent = 2))

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
    nums = [0,0,0]

    for card in std_leg:
        if card['attack'] >= 7:
            nums[0] += 1
        try:
            if 'RUSH' in card['mechanics']:
                nums[1] += 1
        except:
            pass
        if card['attack'] + card['health'] <= 4:
            nums[2] += 1
    print(nums)

    #standard minions
    # a = 0
    # h = 0
    # c = 0
    # for card in std_leg:
    #     a += card['attack']
    #     h += card['health']
    #     c += card['cost']
    # print("Standard Legendaries' averages")
    # print("Mana cost: ", round(c / len(std_leg), 5))
    # print("Attack: ", round(a / len(std_leg), 5), "Health: ", round(h / len(std_leg), 5))
    # print("Stats/Mana: ", round((a / len(std_leg) + h / len(std_leg))/(c / len(std_leg)), 5))
    # a = 0
    # h = 0
    # c = 0
    # for card in leg_minion:
    #     a += card['attack']
    #     h += card['health']
    #     c += card['cost']
    # print("\nWild Legendaries' averages")
    # print("Mana cost: ", round(c/len(leg_minion),5))
    # print("Attack: ", round(a/len(leg_minion),5), "Health: ", round(h/len(leg_minion),5))
    # print("Stats/Mana: ", round((a + h )/ c,5))

    cases = 1000000
    avg = []
    atk = []
    hp = []
    for i in range(cases):
        d = zarogs_round(std_leg)
        stats = []
        for card in d:
            stats.append((card['attack'], card['health']))
        a, b, c = 0, 0, 0
        for j in range(1, 3):
            if stats[j][0] + stats[j][1] > stats[a][0] + stats[a][1]:
                a = j
            if stats[j][0] > stats[b][0]:
                b = j
            if stats[j][1] > stats[c][1]:
                c = j
        avg.append(d[a])
        atk.append(d[b])
        hp.append(d[c])

    sums = [0, 0, 0]
    stats = [[0, 0], [0, 0], [0, 0]]
    x, y = [], []

    for i in range(cases):
        sums[0] += avg[i]['attack'] + avg[i]['health']
        stats[0][0] += avg[i]['attack']
        stats[0][1] += avg[i]['health']
        sums[1] += atk[i]['attack'] + atk[i]['health']
        stats[1][0] += atk[i]['attack']
        stats[1][1] += atk[i]['health']
        sums[2] += hp[i]['attack'] + hp[i]['health']
        stats[2][0] += hp[i]['attack']
        stats[2][1] += hp[i]['health']
        x.append(avg[i]['attack'])
        y.append(avg[i]['health'])

    for i in range(3):
        sums[i] /= cases
        stats[i][0] /= cases
        stats[i][1] /= cases
        sums[i] = round(sums[i], 2)
        stats[i][0] = round(stats[i][0], 2)
        stats[i][1] = round(stats[i][1], 2)

    print("Picking highest weighted stats")
    print("Average total stats:", sums[0])
    print("Attack: ", stats[0][0], "Health: ", stats[0][1])
    print()
    print("Picking highest attack")
    print("Average total stats:", sums[1])
    print("Attack: ", stats[1][0], "Health: ", stats[1][1])
    print()
    print("Picking highest health")
    print("Average total stats:", sums[2])
    print("Attack: ", stats[2][0], "Health: ", stats[2][1])#print statements

    print(x)
    print(y)
    samples = np.array([x, y], np.int32)
    print(type(samples))
    densObj = kde(samples)
    vals = densObj.evaluate(samples)
    norm = Normalize(vmin=vals.min(), vmax=vals.max())
    colours = [cm.ScalarMappable(norm=norm, cmap='jet').to_rgba(val) for val in vals]
    plt.scatter(samples[0], samples[1], color=colours, s = 1000)
    plt.show()

    # with open('wild_data.json', 'w') as outfile:
    #   json.dump(combos[:10000], outfile, indent=2)

if __name__ == '__main__':
    main()