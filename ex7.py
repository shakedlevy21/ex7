import csv

#######################
#Name: Shaked Levy
#EX7
#######################

# Global BST root
ownerRoot = None

########################
# 0) Read from CSV -> HOENN_DATA
########################


def read_hoenn_csv(filename):
    """
    Reads 'hoenn_pokedex.csv' and returns a list of dicts:
      [ { "ID": int, "Name": str, "Type": str, "HP": int,
          "Attack": int, "Can Evolve": "TRUE"/"FALSE" },
        ... ]
    """
    data_list = []
    with open(filename, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=',')  # Use comma as the delimiter
        first_row = True
        for row in reader:
            # It's the header row (like ID,Name,Type,HP,Attack,Can Evolve), skip it
            if first_row:
                first_row = False
                continue

            # row => [ID, Name, Type, HP, Attack, Can Evolve]
            if not row or not row[0].strip():
                break  # Empty or invalid row => stop
            d = {
                "ID": int(row[0]),
                "Name": str(row[1]),
                "Type": str(row[2]),
                "HP": int(row[3]),
                "Attack": int(row[4]),
                "Can Evolve": str(row[5]).upper()
            }
            data_list.append(d)
    return data_list


HOENN_DATA = read_hoenn_csv("hoenn_pokedex.csv")

########################
# 1) Helper Functions
########################
def read_int_safe(prompt):
    while True:
        current = input(prompt)
        if current.lstrip('-').isnumeric():
            return int(current)
        else:
            print("Invalid input.")


def get_poke_dict_by_id(poke_id):
    """
    Return a copy of the Pokemon dict from HOENN_DATA by ID, or None if not found.
    """
    if poke_id < 1 or poke_id > len(HOENN_DATA):
        return None
    new = HOENN_DATA[poke_id-1]
    if new is None:
        return None
    else:
        return new


########################
# 2) BST (By Owner Name)
########################

def create_owner_node(owner_name, first_pokemon):
    """
    Create and return a BST node dict with keys: 'owner', 'pokedex', 'left', 'right'.
    """
    if first_pokemon == 1:
        first_pokemon = HOENN_DATA[0]
    elif first_pokemon == 2:
        first_pokemon = HOENN_DATA[3]
    elif first_pokemon == 3:
        first_pokemon = HOENN_DATA[6]
    owner = {"owner": owner_name, "pokedex": [first_pokemon], "left": None, "right": None}
    insert_owner_bst(ownerRoot, owner)
    print(f"New Pokedex created for {owner_name} with starter {first_pokemon['Name']}.")


def insert_owner_bst(root, new_node):
    """
    Insert a new BST node by owner_name (alphabetically). Return updated root.
    """
    global ownerRoot
    if ownerRoot is None:
        ownerRoot = new_node
        return ownerRoot
    if root is None:
        root = new_node
        return root
    if new_node['owner'].lower() < root['owner'].lower():
        root['left'] = insert_owner_bst(root['left'], new_node)
    elif new_node['owner'].lower() > root['owner'].lower():
        root['right'] = insert_owner_bst(root['right'], new_node)
    else:
        print(f"Owner '{new_node['owner'].lower()}' already exists. No new Pokedex created.")
    return root

def find_owner_bst(root, owner_name):
    """
    Locate a BST node by owner_name. Return that node or None if missing.
    """
    if root is None:
        return None
    if owner_name.lower() == root["owner"].lower():
        return root
    elif owner_name.lower() < root["owner"].lower():
        return find_owner_bst(root["left"], owner_name)
    else:
        return find_owner_bst(root["right"], owner_name)

def get_successor(current):
    if current is None:
        return None
    while current and current.get('left') is not None:
        current = current['left']
    return current

def delete_owner_bst(root, owner_name):
    """
    Removes a node from the BST by owner_name. Return updated root.
    """
    global ownerRoot
    if root is None:
        return
    #find node
    #check for leaf
    if owner_name < root['owner']:
        root['left'] = delete_owner_bst(root['left'], owner_name)
    elif owner_name > root['owner']:
        root['right'] = delete_owner_bst(root['right'], owner_name)
    else:
        # found node to delete
        if root['left'] is None and root['right'] is None:
            if root == ownerRoot:#update ownerRoot
                ownerRoot = None
            return None

        #has only right child
        if root['left'] is None:
            if root == ownerRoot:#update ownerRoot
                ownerRoot = root['right']
            return root['right']

        #has only left child
        if root['right'] is None:
            if root == ownerRoot:#update ownerRoot
                ownerRoot = root['left']
            return root['left']
        else:
            #has two children
            successor = get_successor(root['right'])
            root['owner'] = successor['owner']
            root['pokedex'] = successor['pokedex']
            #delete successor
            root['right'] = delete_owner_bst(root['right'], successor['owner'])


    return root



########################
# 3) BST Traversals
########################

def bfs_traversal(root):
    """
    BFS level-order traversal. Print each owner's name and # of pokemons.
    """
    if root is None:
        return None
    q = [root]
    result = []

    while q:
        len_q = len(q)

        for i in range(len_q):
            # Remove the front of the queue
            node = q.pop(0)  # No alternative to `pop(0)` without imports
            result.append(node)  # Add node to the result list

            # Add left child to the queue
            if node['left'] is not None:
                q.append(node['left'])

            # Add right child to the queue
            if node['right'] is not None:
                q.append(node['right'])

    return result

def pre_order(root):
    """
    Pre-order traversal (root -> left -> right). Print data for each node.
    """
    if root is None:
        return
    print(f"Owner: {root['owner']}")
    q = [i for i in root['pokedex']]
    if q:
        for i in q:
            print(", ".join(f"{key}: {value}" for key, value in i.items()))
    pre_order(root["left"])
    pre_order(root["right"])

def in_order(root):
    """
    In-order traversal (left -> root -> right). Print data for each node.
    """
    if root is None:
        return
    in_order(root["left"])
    print(f"Owner: {root['owner']}")
    q = [i for i in root['pokedex']]
    if q:
        for i in q:
            print(", ".join(f"{key}: {value}" for key, value in i.items()))
    in_order(root["right"])

def post_order(root):
    """
    Post-order traversal (left -> right -> root). Print data for each node.
    """
    if root is None:
        return
    post_order(root["left"])
    post_order(root["right"])
    print(f"Owner: {root['owner']}")
    q = [i for i in root['pokedex']]
    if q:
        for i in q:
            print(", ".join(f"{key}: {value}" for key, value in i.items()))


########################
# 4) Pokedex Operations
########################

def add_pokemon_to_owner(owner_node):
    """
    Prompt user for a Pokemon ID, find the data, and add to this owner's pokedex if not duplicate.
    """
    global HOENN_DATA
    pokemon_id = int(input("Enter Pokemon ID to add: "))
    new_pokemon = get_poke_dict_by_id(pokemon_id)
    if new_pokemon is None:#if is not in the csv file
        print(f"ID {pokemon_id} not found in Honen data.")
        return
    for i in range(len(owner_node['pokedex'])):
        if new_pokemon['ID'] == owner_node['pokedex'][i]['ID']:#check for duplicates
            print("Pokemon already in the list. No changes made.")
            break
    else:
        owner_node['pokedex'].append(new_pokemon)
        print(f"Pokemon {new_pokemon['Name']} "
              f"(ID {new_pokemon['ID']}) added to {owner_node['owner']}'s Pokedex.")

def release_pokemon_by_name(owner_node, name):
    """
    Removes pokemon from this owner's pokedex if found. returns bool
    """
    found = False
    for i in range(len(owner_node['pokedex'])):
        if owner_node['pokedex'][i]['Name'].lower() == name.lower():
            del owner_node['pokedex'][i]
            found = True
            break
    if found is False:
        return False
    else:
        return True

def evolve_pokemon_by_name(owner_node):
    """
    Evolve a Pokemon by name:
    1) Check if it can evolve
    2) Remove old
    3) Insert new
    4) If new is a duplicate, remove it immediately
    """
    name = input("Enter Pokemon Name to evolve: ")
    found = False
    for i in owner_node['pokedex']:
    #check if can evolve
        if i['Name'].lower() == name.lower() and i['Can Evolve'] == 'TRUE':
            temp = get_poke_dict_by_id(i['ID'])#current pokemon
            found = True
            break
    else:#didn't found
        print(f"No Pokemon named '{name}' in {owner_node['owner']}'s Pokedex.")
        return
    if found is False:#can't evolve
        print(f"Pokemon {name} can't evolve.")
        return
    #can evolve and found then we check if the evolved is in the list
    #if it's in the list we delete the original
    #else we append
    evolveded_pokemon = get_poke_dict_by_id(i['ID'] + 1)  # evolved pokemon
    for i in owner_node['pokedex']:
        if i['ID'] == evolveded_pokemon['ID']:
            print(f"Pokemon evolved from {temp['Name']} (ID {temp['ID']}) to"
                  f" {evolveded_pokemon['Name']} (ID {evolveded_pokemon['ID']}).")
            release_pokemon_by_name(owner_node, temp['Name'])
            print(f"\n{evolveded_pokemon['Name']} was already present; releasing it immediately.")
            break
    else:
        release_pokemon_by_name(owner_node, temp['Name'])
        owner_node['pokedex'].append(evolveded_pokemon)
        print(
        f"Pokemon evolved from {temp['Name']} (ID {temp['ID']}) to"
        f" {evolveded_pokemon['Name']} (ID {evolveded_pokemon['ID']}).")


########################
# 5) Sorting Owners by # of Pokemon
########################

def gather_all_owners(root, arr):
    """
    Collect all BST nodes into a list (arr).
    """
    if root is None:
        return

    if root["left"] is not None:
        gather_all_owners(root["left"], arr)
    if root["right"] is not None:
        gather_all_owners(root["right"], arr)
    arr.append(root)
    return arr


def sort_owners_by_num_pokemon():
    """
    Gather owners, sort them by (#pokedex size, then alpha), print results.
    """
    global ownerRoot
    if ownerRoot is None:
        print("No owners at all.")
        return
    print("=== The Owners we have, sorted by number of Pokemons ===\n")
    #arr = []
    #arr = gather_all_owners(ownerRoot, arr)
    arr = bfs_traversal(ownerRoot)
    if arr is None:
        print("failed")
        return

    arr.sort(key=lambda x: (len(x['pokedex']), x['owner'].lower()))

    # size_of_arr = len(arr)
    # for i in range(size_of_arr):
    #     for j in range(0, size_of_arr - i - 1):
    #         #usual bubble sort
    #         if len(arr[j]['pokedex']) > len(arr[j + 1]['pokedex']):
    #             arr[j], arr[j + 1] = arr[j + 1], arr[j]
    #         #if there is the same value check for alphabetical
    #         elif (len(arr[j]['pokedex']) == len(arr[j + 1]['pokedex'])
    #               and arr[j]['owner'].lower() > arr[j + 1]['owner'].lower()):
    #             arr[j], arr[j + 1] = arr[j + 1], arr[j]


    for i in arr:
        print(f"Owner: {i['owner']} (has {len(i['pokedex'])} Pokemon)")


########################
# 6) Print All
########################

def print_all_owners():
    """
    Let user pick BFS, Pre, In, or Post. Print each owner's data/pokedex accordingly.
    """
    global ownerRoot
    while True:
        print('1) BFS\n'
              '2) Pre-Order\n'
              '3) In-Order\n'
              '4) Post-Order\n')
        input_choice = read_int_safe("Your choice: \n")

        if input_choice is None:
            print("Invalid choice. Please try again.")
            continue
        if input_choice == 1:
            bfs_res = bfs_traversal(ownerRoot)
            if bfs_res is None:
                print("No owners at all.")
                continue
            else:
                for i in bfs_res:
                    print(f"Owner: {i['owner']}")
                    for j in i['pokedex']:
                        print(f"ID: {j['ID']}, Name: {j['Name']}, Type: {j['Type']},"
                              f" HP: {j['HP']}, Attack: {j['Attack']},"
                              f" Can Evolve: {j['Can Evolve']}")
            break
        elif input_choice == 2:
            pre_order(ownerRoot)
            break
        elif input_choice == 3:
            in_order(ownerRoot)
            break
        elif input_choice == 4:
            post_order(ownerRoot)
            break


########################
# 7) The Display Filter Sub-Menu
########################

def display_filter_sub_menu(owner_node):
    """
    1) Only type X
    2) Only evolvable
    3) Only Attack above
    4) Only HP above
    5) Only name starts with
    6) All
    7) Back
    """
    while True:
        print("\n-- Display Filter Menu --\n"
              "1. Only a certain Type\n"
              "2. Only Evolvable\n"
              "3. Only Attack above __\n"
              "4. Only HP above __\n"
              "5. Only names starting with letter(s)\n"
              "6. All of them!\n"
              "7. Back\n")

        input_choice = read_int_safe("Your choice: ")
        if input_choice is None:
            print("Invalid choice. Please try again.")
            continue

        if input_choice == 1:
            input_1 = input("Which Type? (e.g. GRASS, WATER): ").lower()
            count = 0
            q = [x for x in owner_node['pokedex'] if x['Type'].lower() == input_1]
            if q:
                for i in q:
                    print(", ".join(f"{key}: {value}" for key, value in i.items()))
            else:
                print("There are no Pokemons in this Pokedex that match the criteria.")

        elif input_choice == 2:
            q = [x for x in owner_node['pokedex'] if x['Can Evolve'] == 'TRUE']
            if q:
                for i in q:
                    print(", ".join(f"{key}: {value}" for key, value in i.items()))
            else:
                print("There are no Pokemons in this Pokedex that match the criteria.")

        elif input_choice == 3:
            attack_above = int(input("Enter Attack threshold: "))
            count = 0
            q = [x for x in owner_node['pokedex'] if x['Attack'] >= attack_above]
            if q:
                for i in q:
                    print(", ".join(f"{key}: {value}" for key, value in i.items()))
            else:
                print("There are no Pokemons in this Pokedex that match the criteria.")

        elif input_choice == 4:
            hp_above = int(input("Enter HP threshold: "))
            q = [x for x in owner_node['pokedex'] if x['HP'] >= hp_above]
            if q:
                for i in q:
                    print(", ".join(f"{key}: {value}" for key, value in i.items()))
            else:
                print("There are no Pokemons in this Pokedex that match the criteria.")
        elif input_choice == 5:
            starting_letters = input("Starting letter(s): ").lower()

            q = [x for x in owner_node['pokedex'] if x['Name'].lower().startswith(starting_letters)]
            if q:
                for i in q:
                    print(", ".join(f"{key}: {value}" for key, value in i.items()))
            else:
                print("There are no Pokemons in this Pokedex that match the criteria.")

        elif input_choice == 6:
            for i in owner_node['pokedex']:
                print(", ".join(f"{key}: {value}" for key, value in i.items()))

        elif input_choice == 7:
            print("Back to Pokedex Menu.")
            break

########################
# 9) Sub-menu & Main menu
########################

def existing_pokedex():
    global ownerRoot
    name = input("Owner name: ").lower()
    current = find_owner_bst(ownerRoot, name)
    if current is None:
        print(f"Owner '{name.lower()}' not found.")
        return
    while True:
        print(f"\n-- {current['owner'].lower()}'s Pokedex Menu --\n",
              "1. Add Pokemon\n",
              "2. Display Pokedex\n",
              "3. Release Pokemon\n",
              "4. Evolve Pokemon\n",
              "5. Back to Main\n")
        choice = read_int_safe("Your choice: ")
        if choice is None:
            print("Invalid choice. Please try again.")
            continue
        if choice == 1:
            add_pokemon_to_owner(current)
        elif choice == 2:
            display_filter_sub_menu(current)
        elif choice == 3:
            name = str(input("Enter Pokemon Name to release: "))
            if not release_pokemon_by_name(current, name):
                print(f"No Pokemon named '{name}' in {current['owner']}'s Pokedex.")
            else:
                print(f"Releasing {name.capitalize()} from {current['owner']}.")
        elif choice == 4:
            evolve_pokemon_by_name(current)
        elif choice == 5:
            print("Back to Main Menu.")
            break
        else :
            print("Invalid choice.")
            continue



def main_menu():
    global ownerRoot
    while True:
        print("=== Main Menu ===\n"
              "1. New Pokedex\n",
              "2. Existing Pokedex\n",
              "3. Delete a Pokedex\n",
              "4. Display owners by number of Pokemon\n",
              "5. Print All\n",
              "6. Exit\n")
        input_choice = read_int_safe("Your choice: ")
        if input_choice is None:
            print("Invalid choice. Please try again.")
            continue
        if input_choice == 1:
            ownername = input("Owner name: ")
            print("Choose your starter Pokemon:\n",
                  "1) Treecko\n",
                  "2) Torchic\n",
                  "3) Mudkip\n")
            starterpokemon = int(input("Your choice: "))
            create_owner_node(ownername, starterpokemon)

        elif input_choice == 2:
            existing_pokedex()
        elif input_choice == 3:
            name = input("Enter owner to delete: ")
            owner = find_owner_bst(ownerRoot, name)
            if owner is None:
                print(f"Owner '{name}' not found.")
                continue
            else:
                print(f"Deleting {owner['owner']}'s entire Pokedex...")
                delete_owner_bst(ownerRoot, name)
                print("Pokedex deleted.")
        elif input_choice == 4:
            sort_owners_by_num_pokemon()
        elif input_choice == 5:
            print_all_owners()
        elif input_choice == 6:
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
            continue

def main():
    main_menu()

if __name__ == "__main__":
    main()
