#Here exists the main storage of the game that can be rented with their corresponding quantity and cost.
game_library = {

    "Donkey Kong": {"quantity": 3, "cost": 2},
    "Super Mario Bros": {"quantity": 5, "cost": 3},
    "Tetris": {"quantity": 2, "cost": 1},
}

user_accounts = {}

'''
The admin has a default username and password.
'''
admin_username = "admin"
admin_password = "adminpass"

#By running this function, it will show the current available games from the game library with complete information.
def display_available_games():

    print("\nHere are the Available Games:")

    for index, (game, details) in enumerate(game_library.items(), 1):
        print(f"{index}. {game}: {details['quantity']} copies available, Rental cost: ${details['cost']}")

'''
In this function, the user will be able to register in order to be able to rent a game.It will require their chosen username and password. For an easy transaction, since the user wants to rent a game, the user will be given a direct top-up of their initial balance in order to rent a game.
'''
def register_user():

    username = input("Kindly enter your username: ")

    if username in user_accounts:
        print("I'm sorry this username already exists. Please input another.")
        return register_user()
    
    else:
        password = input("Kindly enter your password: ")
        balance = float(input("Please make your initial balance. First top-up amount: $"))
        user_accounts[username] = {'password': password, 'balance': balance, 'points': 0, 'inventory': []}
        print("You registered successfully!")
        return username

'''
This function is the main service of this program which is to rent a game. By renting a game, the quantity of the chosen game will be lessen and the balance of the user will decrease according to the cost of the rented game.
'''
def rent_game(username):

    display_available_games()
    game_choice = input("Kindly choose and enter the number of the game you want to rent (leave blank to cancel if ever necessary): ").strip()

    if not game_choice:
        print("Your transaction was cancelled.")
        return
    
    try:
        game_index = int(game_choice) - 1

        if game_index < 0 or game_index >= len(game_library):
            print("Oops! Invalid game number.")
            return rent_game(username)
        game_titles = list(game_library.keys())
        selected_game = game_titles[game_index]

        if game_library[selected_game]['quantity'] == 0:
            print("Apologies, the game you wish to rent is currently out of stock. Feel free to choose another.")
            return
        game_cost = game_library[selected_game]['cost']

        if user_accounts[username]['balance'] < game_cost and user_accounts[username]['points'] < 3:
            print("I'm sorry but you have insufficient balance and points for you to rent this game.")
            return
        
        if user_accounts[username]['points'] >= 3:
            
            user_accounts[username]['points'] -= 3
            print("Congratulations! You have now redeemed enough (3) points for a free game rental.")
            print("You can now rent any game for free.")

        else:

            user_accounts[username]['balance'] -= game_cost
            print(f"Thank you! Game rented successfully! Your remaining balance now is ${user_accounts[username]['balance']}.")
        user_accounts[username]['inventory'].append(selected_game)
        game_library[selected_game]['quantity'] -= 1

    except ValueError:
        print("Oops! Invalid input. Kindly enter a number.")
        return rent_game(username)

''' This function is incharge of managing the returning of a game. First, there should be a rented game which will lead to the inventory. If there exists no game, then the program will print that the user do not have any game in the inventory. By returning the game, the game in the inventory will disappear and will be added to the game library.
'''
def return_game(username):

    if not user_accounts[username]['inventory']:
        print("It looks like you don't have any games to return as of now.")
        return
    print("\nHere are the current games in your inventory:")

    for index, game in enumerate(user_accounts[username]['inventory'], 1):
        print(f"{index}. {game}")
    game_choice = input("Kindly the number of the game you want to return (leave blank to cancel if ever necessary): ").strip()

    if not game_choice:
        print("Your transaction was cancelled.")
        return
    
    try:

        game_index = int(game_choice) - 1

        if game_index < 0 or game_index >= len(user_accounts[username]['inventory']):
            print("Oops! Invalid game number.")
            return return_game(username)
        returned_game = user_accounts[username]['inventory'].pop(game_index)
        game_library[returned_game]['quantity'] += 1
        print("Thank you! The game returned successfully!")

    except ValueError:
        print("Oops! Invalid input. Kindly enter a number.")
        return return_game(username)

'''
In this function, the user is given a chance to top-up or add balance to their account. It will require only positive numbers since it will only accept positive whole numbers or money. By entering the desired amount, it will automatically add to the current balance of the user.
'''
def top_up_account(username, amount):

    try:
        amount = float(amount)

        if amount <= 0:
            print("I'm sorry but you input an invalid amount. Kindly enter a positive number.")
            return
        user_accounts[username]['balance'] += amount
        print(f"Your account has topped up successfully! Your new balance is: ${user_accounts[username]['balance']}.")

    except ValueError:
        print("Oops! Invalid input. Kindly enter a number.")

#Here is the function that will show the inventory of the user. It contains games that are rented. It will simply make it display the rented games.
def display_inventory(username):

    if user_accounts[username]['inventory']:
        print("\nHere are the current games in your inventory:")

        for game in user_accounts[username]['inventory']:
            print(game)

    else:
        print("Looks like you don't have any games in your inventory as of now.")

#This function is only applicable if the program handling it is the admin. Here, the admin is free to update the games quantities and costs.
def admin_update_game():

    if not admin_login():
        return
    display_available_games()
    game_choice = input("Kindly the number of the game you want to update (leave blank to cancel if necessary): ").strip()

    if not game_choice:
        print("Your transaction was cancelled.")
        return
    
    try:
        game_index = int(game_choice) - 1

        if game_index < 0 or game_index >= len(game_library):
            print("Oops! Invalid game number.")
            return admin_update_game()
        game_titles = list(game_library.keys())
        selected_game = game_titles[game_index]
        new_quantity = int(input("Kindly the new quantity: "))
        new_rental_cost = float(input("Now enter the new rental cost: $"))
        game_library[selected_game]['quantity'] = new_quantity
        game_library[selected_game]['cost'] = new_rental_cost
        print("The game details has now been updated!")

    except ValueError:
        print("Oops! Invalid input. Kindly enter a number.")
        return admin_update_game()

'''
This is the function that will allow the admin to access the rental control. The admin shall enter the right default username and password for the program to confirm the admin.
'''
def admin_login():

    username = input("Kindly enter admin username: ")
    password = input("Kindly enter admin password: ")

    if username == admin_username and password == admin_password:
        print("Admin login successful!")
        return True
    
    else:
        print("Oops! Looks like the admin credentials are invalid .")
        return False

#The function admin_menu shows the action that the admin can do, which is to update the game informations.
def admin_menu():

    while True:
        print("\nWelcome dear Admin to the Admin Menu! What would you like to do:")
        print("1. Update game details\n2. Exit")
        
        choice = input("Kindly enter your choice: ")

        if choice == '1':
            admin_update_game()

        elif choice == '2':
            print("Now exiting admin menu.")
            break

        else:
            print("Oops! Invalid choice. Please try again.")

'''
This is a special function since it is a special service of the program for the users that rented certain amount of games. The user can redeem a free rental game when they reach 3 points. A point is equivalent when the user purchased or spent 2$.
'''
def redeem_free_rental(username):

    if user_accounts[username]['points'] >= 3:
        print("Congratulations! You have now redeemed enough (3) points for a free game rental.")
        print("You can now redeem your points for a free rental of any game! Thank you for trusting our service!")
        rent_game(username)
        user_accounts[username]['points'] -= 3

    else:
        print("I'm sorry, but it looks like you don't have enough points to redeem a free game rental for now.")

#This functions simply displays the inventory of the games.
def display_game_inventory():

    print("\nGame Inventory:")

    for game, details in game_library.items():
        print(f"{game}: {details['quantity']} copies available")

'''This function is available when the user finally registered. Here consists the access to rent a game, return a game, top-up, display the inventory, redeem points, and check points.
'''
def logged_in_menu(username):

    while True:
        print("\nLogged-in Menu:")
        print("1. Rent a game\n2. Return a game\n3. Top-up account\n4. Display inventory\n5. Redeem points for a free rental\n6. Check points\n7. Exit")
        
        choice = input("Kindly enter your choice: ")
        if choice == '1':
            rent_game(username)
        elif choice == '2':
            return_game(username)
        elif choice == '3':
            amount = input("Kindly enter the amount to top up: $")
            top_up_account(username, amount)
        elif choice == '4':
            display_inventory(username)
        elif choice == '5':
            redeem_free_rental(username)
        elif choice == '6':
            display_points(username)
        elif choice == '7':
            print("Exiting logged-in menu.")
            break
        else:
            print("Oops! Invalid choice. Please try again.")

#This function simply confirms every username that is registered is existing and their password, and if they match with each other.
def check_credentials(username, password):

    if username in user_accounts and user_accounts[username]['password'] == password:
        return True
    
    else:
        return False
    
#The display_points function shows the current existing points of the user from the past interactions in the rental system.
def display_points(username):

    print(f"Your current points for {username}: {user_accounts[username]['points']}")

#This is the main function. This is the first display of the program and will start everything.
def main():

    while True:

        print("\nWelcome to the Video Game Rental System!")
        print("1. Register as a new user\n2. Log in\n3. Admin login\n4. Exit")
        
        choice = input("Kindly enter your choice: ")

        if choice == '1':
            username = register_user()
            if username:
                logged_in_menu(username)
        elif choice == '2':
            username = input("Kindly enter your username: ")
            password = input("Kindly enter your password: ")
            if check_credentials(username, password):
                logged_in_menu(username)
            else:
                print("Oops! Invalid username or password.")
        elif choice == '3':
            if admin_login():
                admin_menu()
        elif choice == '4':
            print("Thank you for using the Video Game Rental System. Goodbye! Hope to be of your service again!")
            break
        else:
            print("Oops! Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
