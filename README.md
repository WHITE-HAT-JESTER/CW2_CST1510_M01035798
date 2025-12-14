

# CST1510 – Coursework 2  
## Multi-Domain Intelligence Platform

>**Module:** CST1510 – BSC. CYBERSECURITY AND DIGITAL FORENSICS  
**Student Name:** Hindu Nabbosa
**Student ID:** M01035798 
**Institution:** Middlesex University Mauritius  
**Assessment Type:** Coursework 2  

---

## Project Overview

This project is a **Multi-Domain Intelligence Platform** developed using **Python**, **Streamlit**, **SQLite**, and **Pandas**.  
It brings together the main concepts covered throughout the module and applies them in a single platform.

The platform is designed to support **two operational domains**:

- **Cybersecurity**
-  **IT Operations**

Each domain provides data management, analytics, and decision-support features.

##  Git & Project Setup

During Week 6, the project foundation was established:

- GitHub repository creation and management
- Clear separation of concerns between UI, services, and data layers
- Use of `.gitignore` to exclude virtual environments and secrets
- Incremental commits following good version control practices

---

## Authentication & Security



A command line authentication system implementing secure password hashing. 
This system allows users to register accounts and log in with proper password and
usernames.

> FEATURES

•Secure password hashing using bcrypt with automatic salt generation

•User registration with duplicate username prevention

•User login with Password Verification

•Input validation for usernames and passwords

•File-based user data persistence

>TECHNICAL IMPLEMENTATION

•Hashing Algorithm: bcrypt with automatic salting

•Data Storage: Plain Text file(`users.txt`) with comma-seperated values

•Password Security: One-Way Hashing, no plaintext storage

•Validation: Username (3-25 alphanumeric characters), Password(8-30 characters)

---

## Database Design & CRUD Operations

The platform uses **SQLite** as its database backend.

>FEATURES

- Centralised database connection handling
- Structured database schema
- Domain-specific data tables for users, incidents, datasets, and IT tickets
- Full CRUD (Create, Read, Update, Delete) functionality
- Initial data loading from CSV files
- Clear separation between database logic and Streamlit UI pages

This ensures data consistency and simplifies future extensions.

---

## Data Analytics & Visualisation


>FEATURES

- Export of filtered data to CSV
- Domain-specific insights to support decision-making


## Security and Development Practices

The project follows good security  practices:

- No secrets file uploaded on git
- Graceful error handling throughout the application
- Modular architecture for improved maintainability
- Clear and detailed inline comments for academic clarity

---

## How to Run the Project

1. Activate the virtual environment  
2. Install dependencies using `requirements.txt`  
3. Run the application using Streamlit  

The application runs locally and is accessible via a web browser.

---