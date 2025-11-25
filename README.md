[README.md](https://github.com/user-attachments/files/23734945/README.md)
# WEEK 7: SECURE AUTHENTICATION SYSTEM
 
>Student Name: Hindu Nabbosa

>Student ID: M01035798

>Course: CST1510-CW2-MULTIDOMAIN INTELLIGENCE PLATFORM

### PROJECT DESCRIPTION

A command line authentication system implementing secure password hashing. 
This system allows users to register accounts and log in with proper password and
usernames.

### FEATURES

-Secure password hashing using bcrypt with automatic salt generation

-User registration with duplicate username prevention

-User login with Password Verification

-Input validation for usernames and passwords

-File-based user data persistence

### TECHNICAL IMPLEMENTATION

-Hashing Algorithm: bcrypt with automatic salting

-Data Storage: Plain Text file(`users.txt`) with comma-seperated values

-Password Security: One-Way Hashing, no plaintext storage

-Validation: Username (3-25 alphanumeric characters), Password(8-30 characters)
