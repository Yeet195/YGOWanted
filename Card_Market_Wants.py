'''

Development startet on March 4th 2024

'''

from time import sleep
import sys
import re
import requests

a = input("Sort by low rarity (Y/N)").strip().lower()
if a == "y":
    rarity_hierarchy = {'Common': 6,
                        'Rare': 5,
                        'Super Rare': 4,
                        'Ultra Rare': 3,
                        'Prismatic Secret Rare': 2,
                        'Secret Rare': 1}
else: 
    rarity_hierarchy = {'Ultimate Rare': 11,
                        'Starlight Rare': 10,
                        'Ghost Rare': 9,
                        'Quarter Century Secret Rare': 8,
                        'Collector\'s Rare': 7,
                        'Secret Rare': 6,
                        'Prismatic Secret Rare': 5,
                        'Ultra Rare': 4,
                        'Super Rare': 3,
                        'Rare': 2,
                        'Common': 1}

def fetch_rarity(card_name):
    api_card_name = card_name.split('&')[0].strip()

    url = f"https://db.ygoprodeck.com/api/v7/cardinfo.php?name={api_card_name}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        card_sets = data['data'][0].get('card_sets', [])
        
        if card_sets:
            highest_rarity_set = max(card_sets, key=lambda x: rarity_hierarchy.get(x['set_rarity'], 0))
            
            count_in_highest_rarity_set = card_sets.count(highest_rarity_set)
            if count_in_highest_rarity_set > 1:
                if a == "y":
                    count_in_highest_rarity_set = count_in_highest_rarity_set - (count_in_highest_rarity_set - 1)
                return f"(V.{count_in_highest_rarity_set}) ({highest_rarity_set['set_name']})"
            else:
                return f"({highest_rarity_set['set_name']})"
                
    return ""

def extract_cards(deck_list):
    lines = deck_list.strip().replace('\r', '').split('\n')[1:]
    cards = []
    for line in lines:
        card_info = re.match(r"(\d+)x (.+)$", line)
        if card_info:
            count = int(card_info.group(1))
            card_name = card_info.group(2).strip()
            cards.append((count, card_name))
    return cards

def main():
    file_path = "your_deck_list.txt"

    with open(file_path, 'r', encoding='utf-8') as file:
        deck_list = file.read()

    main_deck_cards = extract_cards(deck_list)

    wants_list = []
    error_cards = []

    for index, (count, card_name) in enumerate(main_deck_cards, start=1):
        progress = int((index / len(main_deck_cards)) * 100)
        sys.stdout.write('\r')
        sys.stdout.write("[%-100s] %d%%" % ("\u25A0" * progress, progress))
        sys.stdout.flush()

        highest_rarity_set = fetch_rarity(card_name)
        if highest_rarity_set == "":
            wants_list.append(f"{count} {card_name}")
            error_cards.append(f"{card_name}")
        else:
            wants_list.append(f"{count} {card_name} {highest_rarity_set}")

        sleep(0.01)

    sys.stdout.write('\n')

    wants_list_output = '\n'.join(wants_list)

    with open("wants_list.txt", 'w', encoding='utf-8') as output_file:
        output_file.write(wants_list_output)

    if len(error_cards) == 0:
        print("Wants list created.")
    else:
        print(f"Wants list created with the following cards missing:\n {error_cards}")

if __name__ == "__main__":
    main()