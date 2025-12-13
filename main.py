from app.data.db import DB_PATH, connect_database
from app.data.schema import create_all_tables,load_all_csv_data, CSV_PATHS
from app.services.user_service import register_user, login_user, migrate_users_from_file
from app.data.incidents import insert_incident, get_all_incidents

def main():
    print("=" * 60)
    print("Week 8: Database Demo")
    print("=" * 60)

    # 1. Setup database
    conn = connect_database()
    create_all_tables(conn)
    conn.close()

    # 2. Migrate users
    migrate_users_from_file()

    # 3. Test authentication
    success, msg = register_user("ulia", "SecurePass123!", "analyst")
    print(msg)

    success, msg = login_user("ulia", "SecurePass123!")
    print(msg)

    # 4. Test CRUD
    incident_id = insert_incident(
        "2024-11-05",
        "Phishing",
        "High",
        "Open",
        "Suspicious email detected",
        "alice"
    )
    print(f"Created incident #{incident_id}")



    # 5. Query data
    df = get_all_incidents()
    print(f"Total incidents: {len(df)}")

def demonstrate_all_crud():
    """Show CRUD for all 3 domains """
    print("\n" + "=" * 60)
    print("DEMONSTRATING CRUD FOR ALL 3 DOMAINS")
    print("=" * 60)

    # 1. CYBERSECURITY DOMAIN
    print("\n1. CYBERSECURITY:")
    print("   Create: Insert new incident")
    incident_id = insert_incident("2024-11-10", "DDoS", "High", "Open", "Test DDoS attack", "admin")
    print(f"   Read: Get all incidents ({len(get_all_incidents())} total)")
    print("   Update: Would update status here")
    print("   Delete: Would delete incident here")

    # 2. DATA SCIENCE DOMAIN
    print("\n2. DATA SCIENCE:")
    print("   Create: Insert new dataset")
    # You need to import datasets functions
    from app.services.datasets import insert_dataset
    dataset_id = insert_dataset("Test_Dataset", "Test", "Manual", "2024-11-10", 100, 5.0, "admin", "2024-11-10")
    print(f"   Created dataset #{dataset_id}")

    # 3. IT OPERATIONS DOMAIN
    print("\n3. IT OPERATIONS:")
    print("   Create: Insert new ticket")
    # You need to import tickets functions
    from app.services.tickets import insert_ticket
    ticket_id = insert_ticket("T9999", "Medium", "Test Ticket", "Testing CRUD", "IT_Support_A", "General", "Open", None)
    print(f"Created ticket #{ticket_id}")

    print("\nAll 3 domains have CRUD operations implemented!")

def setup_database_complete():
    """
    Complete database setup:
    1. Connect to database
    2. Create all tables
    3. Migrate users from users.txt
    4. Load CSV data for all domains
    5. Verify setup
    """
    print("\n" + "=" * 60)
    print("STARTING COMPLETE DATABASE SETUP")
    print("=" * 60)

    # Step 1: Connect
    print("\n[1/5] Connecting to database...")
    conn = connect_database()
    print("       Connected")

    # Step 2: Create tables
    print("\n[2/5] Creating database tables...")
    create_all_tables(conn)

    # Step 3: Migrate users
    print("\n[3/5] Migrating users from users.txt...")
    user_count = migrate_users_from_file()
    print(f"Migrated {user_count} users")


    # Step 4: Load CSV data
    print("\n[4/5] Loading CSV data...")
    csv_paths_map = CSV_PATHS
    total_rows = load_all_files(conn, csv_paths_map)

    # Step 5: Verify
    print("\n[5/5] Verifying database setup...")
    cursor = conn.cursor()

    # Count rows in each table
    tables = ['users', 'cyber_incidents', 'datasets_metadata', 'it_tickets']
    print("\n Database Summary:")
    print(f"{'Table':<25} {'Row Count':<15}")
    print("-" * 40)

    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"{table:<25} {count:<15}")

    conn.close()

    print("\n" + "=" * 60)
    print(" DATABASE SETUP COMPLETE!")
    print("=" * 60)
    print(f"\n Database location: {DB_PATH.resolve()}")
    print("\nYou're ready for Week 9 (Streamlit web interface)!")


# Run the complete setup
if __name__ == "__main__":
    main()
