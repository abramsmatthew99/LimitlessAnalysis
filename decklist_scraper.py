import os
import collections

folder_path = './Regional Goiania'
file_names = os.listdir(folder_path)

card_counts_per_archetype = collections.defaultdict(list)

for file_name in file_names:
    # Split the file name to get the player's name and archetype
    print(file_name)
    player_name, archetype = file_name.split("-")

    # Read the file line by line and process the data
    with open(os.path.join(folder_path, file_name), "r") as file:
        lines = file.readlines()

        for line in lines:
            #Check if this line contains a card or not, since all cards start with their quantity
            if not line[0].isnumeric():
                continue
            # Extract the card information (e.g., 2x Pikachu)
            card_info = line.strip()

            # Split the card information to get the card name and quantity
            split_info = card_info.split(" ")
            quantity = int(split_info[0])
            card_name = " ".join(split_info[1:])

            # Increment the count of this card for the current archetype
            card_counts_per_archetype[card_name].append(quantity)

for card_name, counts in card_counts_per_archetype.items():
    total_count = sum(counts)
    average_count = total_count // len(counts)
    print(f"{card_name}: {average_count}")