import csv

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
    current = input(prompt)
    if current.isdigit():
        return int(current)
    else:
        return None

def get_poke_dict_by_id(poke_id):
    """
    Return a copy of the Pokemon dict from HOENN_DATA by ID, or None if not found.
    """
    return HOENN_DATA[poke_id-1]

def get_poke_dict_by_name(name):
    """
    Return a copy of the Pokemon dict from HOENN_DATA by name, or None if not found.
    """
    return HOENN_DATA[name]

def display_pokemon_list(poke_list):
    """
    Display a list of Pokemon dicts, or a message if empty.
    """
    pass


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
    if new_node["owner"].lower() < root["owner"].lower():
        root["left"] = insert_owner_bst(root["left"], new_node)
    elif new_node["owner"].lower() > root["owner"].lower():
        root["right"] = insert_owner_bst(root["right"], new_node)
    else:
        print(f"Owner '{new_node["owner"].lower()}' already exists. No new Pokedex created.")
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

def min_node(current):
    """
    Return the leftmost node in a BST subtree.
    """
    while current is not None and current.left is not None:
        current = current.left
    return current

def get_successor(current):
    current = current.right
    while current is not None and current.left is not None:
        current = current.left
    return current

def delete_owner_bst(root, owner_name):
    """
    Removes a node from the BST by owner_name. Return updated root.
    """
    ## If key to be searched is in a subtree

        # If root matches with the given key

        # Cases when root has 0 children or
        # only right child
    if root['left'] is None:
        return root['right']

    # When root has only left child
    if root['right'] is None:
        return root['left']

    # When both children are present
    succ = get_successor(root)
    root.key = succ.key
    root.right = delete_owner_bst(root.right, succ.key)

    return root



########################
# 3) BST Traversals
########################

def bfs_traversal(root):
    """
    BFS level-order traversal. Print each owner's name and # of pokemons.
    """

    if root is None:
        return []
    q = [root]
    res = []

    current_level = 0

    while q:
        len_q = len(q)
        res.append([])

        for i in range(len_q):
            # Add front of queue and remove it from queue
            node = q.append()
            res[current_level].append(node.data)

            # Enqueue left child
            if node.left is not None:
                q.append(node.left)

            # Enqueue right child
            if node.right is not None:
                q.append(node.right)
        current_level += 1

    return res

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
            print(print(", ".join(f"{key}: {value}" for key, value in i.items())))
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
            print(print(", ".join(f"{key}: {value}" for key, value in i.items())))
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
            print(print(", ".join(f"{key}: {value}" for key, value in i.items())))


########################
# 4) Pokedex Operations
########################

def add_pokemon_to_owner(owner_node):
    """
    Prompt user for a Pokemon ID, find the data, and add to this owner's pokedex if not duplicate.
    """
    global HOENN_DATA
    pokemon_id = int(input("Enter Pokemon ID to add: ")) - 1
    new_pokemon = get_poke_dict_by_id(pokemon_id)
    if new_pokemon is None:#if is not in the csv file
        print(f"Pokemon ID {pokemon_id} not found.")
        return
    for i in range(len(owner_node["pokedex"])):
        if HOENN_DATA[pokemon_id]["ID"] == owner_node["pokedex"][i]["ID"]:#check for duplicates
            print("Pokemon already in the list. No changes made.")
            break
    else:
        owner_node["pokedex"].append(HOENN_DATA[pokemon_id])
        print(f"Pokemon {HOENN_DATA[pokemon_id]["Name"]} "
              f"(ID {HOENN_DATA[pokemon_id]["ID"]}) added to {owner_node["owner"]}'s Pokedex.")

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
            #check for duplicates
            temp = get_poke_dict_by_id(i['ID'] + 1)
            if release_pokemon_by_name(owner_node, temp['Name']):#check if it released
                print(f"{i['Name']} was already present; releasing it immediately.")
            #evolve
            print(f"Pokemon evolved from {i['Name']} (ID {i['ID']}) to {temp['Name']} (ID {temp['ID']}).")
            i['Name'] = temp['Name']
            i['ID'] = temp['ID']
            i['Can Evolve'] = temp['Can Evolve']
            i['Type'] = temp['Type']
            i['HP'] = temp['HP']
            i['Attack'] = temp['Attack']
            found = True
            break
    if found is False:
        print(f"Pokemon {name} can't evolve.")

########################
# 5) Sorting Owners by # of Pokemon
########################

def gather_all_owners(root, arr):
    """
    Collect all BST nodes into a list (arr).
    """
    arr.append(root)
    if root["left"] is not None:
        gather_all_owners(root["left"], arr)
    if root["right"] is not None:
        gather_all_owners(root["right"], arr)
    return arr


def sort_owners_by_num_pokemon():
    """
    Gather owners, sort them by (#pokedex size, then alpha), print results.
    """
    global ownerRoot
    if ownerRoot is None:
        print("No owners at all.")
        return
    arr = []
    arr = gather_all_owners(ownerRoot, arr)
    if arr is None:
        print("failed")
        return
    arr.sort(key=lambda x: (len(x['pokedex']), x['owner']))
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
        input_choice = read_int_safe("Your choice: ")

        if input_choice is None:
            print("Invalid choice. Please try again.")
            continue
        if input_choice == 1:
            print("BFS Traversal:")
            bfs_res = bfs_traversal(ownerRoot)
            for i in bfs_res:
                print(", ".join(f"{key}: {value}" for key, value in i))
            break
        elif input_choice == 2:
            print("Pre-Order Traversal:")
            pre_order(ownerRoot)
            break
        elif input_choice == 3:
            print("In-Order Traversal:")
            in_order(ownerRoot)
            break
        elif input_choice == 4:
            print("Post-Order Traversal:")
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
        print("-- Display Filter Menu --\n"
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
            q = [x for x in owner_node['pokedex'] if x['HP'] >= attack_above]
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
        print(f"-- {current["owner"].lower()}'s Pokedex Menu --\n",
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
            name = str(input("Enter Pokemon name to release: ").lower())
            if not release_pokemon_by_name(current, name):
                print(f"No Pokemon named '{name}' in {current['owner']}'s Pokedex.")
            else:
                print(f"Releasing {name} from {current['owner']}.")
        elif choice == 4:
            evolve_pokemon_by_name(current)
        elif choice == 5:
            break
        else :
            print("Invalid choice. Please try again.")
            continue



def main_menu():
    global ownerRoot
    while True:
        print("=== Main Menu ===\n"
              "1) New Pokedex\n",
              "2) Existing Pokedex\n",
              "3) Delete a Pokedex\n",
              "4) Display owners by number of Pokemon\n",
              "5) Print all\n",
              "6) Exit\n")
        input_choice = read_int_safe("Enter your choice: ")
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
            delete_owner_bst(owner, name)
        elif input_choice == 4:
            sort_owners_by_num_pokemon()
        elif input_choice == 5:
            print_all_owners()
        elif input_choice == 6:
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")
            continue

def main():
    main_menu()
    print(ownerRoot)

if __name__ == "__main__":
    main()
