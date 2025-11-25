import bcrypt
import os
import re


USER_DATA_FILE = "users.txt"


#hashes a password using bcrypt with automatic salt generation.
#Args:
#plain_text_password(str): the plaintext password to hash.
#Returns:
#str: the hashed password as a UTF-8 string

def hash_password(password: str) -> str:
    #TO DO: Encode the password to bytes(bcrypt requires byte strings)
    password_bytes = password.encode("utf-8")

    #TO DO: Generate a salt using bcrypt.gensalt()
    salt = bcrypt.gensalt(rounds=12)  #no. of rounds for cost factor determine the processing speed it takes to login
    print(salt)

    #TO DO: Hash the password using bcrypt.hashpw()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    print("Password: ", password)
    print("Hashed: ", hashed_password)

    #TO DO: Decode the hash back to a string to store in a text file.
    return hashed_password.decode(
        "utf-8")  #this is important because later when you verify if you don't do it, you'll get a TypeError. since hashed_password becomes none, as it doesn't return anything and return requires values.


def verify_password(password: str, hashed_password: str) -> bool:
    #TO DO: Encode both the plaintext password and the stored hash to bytes
    #TO DO: Use bcrypt.checkpw() to check password
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))
    #this function extracts salt from the hash and compares


#ARGS:
#plain_text_password(str): password to verify
#hashed_password(str): stored hash to compare to
#RETURNS:
#bool: true if matched, false if password unmatched.


def register_user(username, password):
    hashed_password = hash_password(password)

    if not os.path.exists(USER_DATA_FILE):
        open(USER_DATA_FILE, "w").close()  #creates an empty file

    #TO DO: Check if the username  already exists.
    #start off by checking if file exists. if not, initialize an empty list
    with open(USER_DATA_FILE, "r") as file:
        lines = file.readlines()
    for line in lines:
        saved_username = line.split(",")[0].strip()

        if saved_username == username:
            print(f"User {username} already exists")
            return False

    #TO DO: Append the new user to the file
    # #TO DO: Hash the Password
    # #this means the file will open with append mode enabled
    with open("users.txt", "a") as f:
        f.write(f"{username},{hashed_password}\n")
    return True


def login_user(username,password):
    #TO DO: Handle the case where no users are registered yet
    if not(os.path.exists(USER_DATA_FILE)):
        print("No users registered yet")
        return False
    saved_username = username
    #TO DO: Search for the username in the file
    with open(USER_DATA_FILE, "r") as file:
        for line in file.readlines():
            [username, saved_hash] = line.strip().split(',', 1)
            #TO DO: If username matches, verify the password
            if username == saved_username:
                if verify_password(password, saved_hash):
                    print(f"Logged in as '{saved_username}'")
                    return True
                else:
                    print(f"Wrong password!")
                    return False
        print("Username not found")
        return False

#TO DO:Validate username format
def validate_username(username):
    while True:
        if not(3<=len(username)<=25):
            return False, "Username must be between 3 and 25 characters long"
        pattern = r"^[a-zA-Z0-9]+$"
        if re.match(pattern, username):
            return True, None
        return False, print(f"User '{username}' is not a valid username.")
pass

def validate_password(password):
    while True:
        if not(8<= len(password) <=30):
            return False, "Password must be between 8 and 30 characters long."

        l = u = d = p = 0
        for char in password:
            if char.islower():
                l += 1
            elif char.isupper():
                u += 1
            elif char.isdigit():
                d += 1
            elif char.isspace():
                p += 1
        if l>=1 and u>=1 and d>=1:
            print("Strong password")
            return True, None
        return False, "Invalid Password. Password must contain at least one uppercase, one lowercase and one digit."

pass

#Implement the Main Menu
def display_menu():
    """Display menu options"""
    print("\n"+"_"*50)
    print("MULTI-DOMAIN INTELLIGENCE PLATFORM")
    print("_"*50)
    print("WELCOME")
    print("\n1. Register")
    print("\n2. Login")
    print("\n3. Exit")
    print("_"*50)

def main():
    """Main function/ Main program loop"""
    print("\nWelcome to Multi-Domain Intelligence Platform")
    while True:
        display_menu()
        option = input("Option: ").strip()
        if option == "1":
            #Registration Flow
            print("\n---REGISTRATION---")
            username = input("Username: ").strip()
            password = input("Password: ")
            confirm = input("Confirm password: ")

            #Validate Username
            is_valid, error = validate_username(username)
            if not is_valid:
                print(f"Error: {error}")
                continue
            #Validate password
            is_valid, error = validate_password(password)
            if not is_valid:
                print(f"Error: {error}")
                continue
            if confirm != password:
                print(f"Error: Passwords don't match.")
                continue

            #Register the user
            if register_user(username, password):
                print(f"'{username}' registered successfully")
            else:
                print(f"Error: {username} already exists.")
                continue

        elif option == "2":
            #Login Flow
            print("\n---LOGIN---")
            username = input("Username: ").strip()
            password = input("Password: ").strip()

            #Attempt Login
            if login_user(username, password):
                print(f"Hello '{username}'!")
            else:
                print("Login Failed. Invalid Username or Password.")
                input("\nPress Enter to try again or ESC to exit...")
                continue

        elif option == "3":
            #Exit
            print("Exiting...")
            break

        else:
            print("\nInvalid option. Please try again.")

if __name__ == "__main__":
    main()
