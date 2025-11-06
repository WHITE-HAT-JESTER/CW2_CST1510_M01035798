import bcrypt
import os

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
    return hashed_password.decode("utf-8")  #this is important because later when you verify if you don't do it, you'll get a TypeError. since hashed_password becomes none, as it doesn't return anything and return requires values.


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
        open(USER_DATA_FILE, "w").close() #creates an empty file

    #TO DO: Check if the username  already exists.
    #start off by checking if file exists. if not, initialize an empty list
    with open(USER_DATA_FILE, "r") as file:
        lines = file.readlines()
    for line in lines:
        saved_username = line.split(":")[0].strip()

        if saved_username != username:
            print(f"User '{username}' registration complete.")
        else:
            print(f"User {username} already exists")
            print(f"User '{username}' registration failed.")

    #TO DO: Append the new user to the file
    # #TO DO: Hash the Password
    # #this means the file will open with append mode enabled
    with open("users.txt", "a") as f:
        f.write(f"{username},{hashed_password}\n")
    return True


def login_user(username, password):
    hashed_password = hash_password(password)
    saved_username = username
    with open(USER_DATA_FILE, "r") as file:
      for line in file.readlines():
          username,saved_hash = line.strip().split(',', 1)
          if username == saved_username:
            if verify_password(password, hashed_password):
                print(f"Logged in as '{saved_username}'")
            else:
              print(f"Wrong password!")
          return False
    return login_user(username, password)


if __name__ == "__main__":  #Means to only run the code if the file is not imported from elsewhere.
    print("Enter your username and password.\n")
    username=input("Username: ")
    password=input("\nPassword: ")
    register_user(username, password)

    print("TESTING LOGIN\n")
    username = input("Username: ")
    password = input("\nPassword: ")
    login_user(username, password)

    exit(1)

