from db import DB_PATH, connect_database
from schema import create_all_tables, load_all_csv_data, CSV_PATHS
import schema as schema
from my_app.services.user_service import register_user, login_user, migrate_users_from_file
from incidents import insert_incident, get_all_incidents,update_incident_status, delete_incident
from datasets import insert_dataset, get_all_datasets, update_dataset_record_count, delete_dataset
from tickets import insert_ticket, get_all_tickets,update_ticket_status, delete_ticket
from users import insert_user, get_all_users,delete_user, check_username_exists


def main():
    print("=" * 60)
    print("Week 8: Database Demo")
    print("=" * 60)

    # 1. Setup database
    conn = connect_database()
    create_all_tables(conn)
    conn.close()

    # 2. Migrate users
    user_count=migrate_users_from_file()
    print(f"User count: {user_count}")

    # Check and migrate legacy incident schema if available
    try:
        if hasattr(schema, 'migrate_cyber_incidents_table'):
            migrated = schema.migrate_cyber_incidents_table(connect_database())
            if migrated:
                print("Applied migration: cyber_incidents schema")
        else:
            print("No legacy-schema migration function available; skipping.")
    except Exception as e:
        print(f"Schema migration check failed: {e}")

    # 3. Test authentication
    success, msg = register_user("ulia", "SecurePass123!", "analyst")
    print(msg)

    success, msg = login_user("ulia", "SecurePass123!")
    print(msg)

    # 4. Test CRUD
    print("\n"+"=" * 60)
    print("TESTING CRUD OPERATIONS")
    print("=" * 60)

    ##CYBERSECURITY
    print("\n1. CYBERSECURITY:")
    print("-"*40)
    incident_df=get_all_incidents()
    print(f"{len(incident_df)} incidents found")
    incident_id = insert_incident(
        "2024-11-05",
        "Phishing",
        "High",
        "Open",
        "Suspicious email detected",
        "alice"
    )
    if incident_id:
        print(f"Created incident #{incident_id}")
    else:
        print("Failed to create incident")

    incident_df = get_all_incidents()
    print(f"Total incidents after insertion: {len(incident_df)}")

    if len(incident_df) > 0:
        print("\nSample incident data:")
        print(incident_df.head())

    ##DATASETS
    print("\n2. DATASETS:")
    print("-" * 40)
    datasets_df = get_all_datasets()
    print(f"{len(datasets_df)} datasets found")
    dataset_id = insert_dataset(
        "Customer_Analytics_2024",
        "Analytics",
        "Internal",
        "2024-11-05",
        10000,
        25.5,
        "data_scientist",
        "2024-11-05 10:00:00"
    )
    if dataset_id:
        print(f"Created dataset #{dataset_id}")

    datasets_df = get_all_datasets()
    print(f"Total datasets: {len(datasets_df)}")

    if len(datasets_df) > 0:
        print("\nSample dataset data:")
        print(datasets_df.head())

    ##IT USERS
    print("\n3. IT_TICKETS:")
    print("-" * 40)
    tickets_df = get_all_tickets()
    print(f"{len(tickets_df)} tickets found")
    test_ticket_id = "T9999"
    ticket_row_id = insert_ticket(
        test_ticket_id,
        "Medium",
        "Test Ticket",
        "Network issue",
        "IT_Support_A",
        "Network",
        "Open",
        None,
        "2024-11-05 09:00:00"
    )
    if ticket_row_id:
        print(f"Created ticket #{ticket_row_id}")

    tickets_df = get_all_tickets()
    print(f"Total tickets: {len(tickets_df)}")

    if len(tickets_df) > 0:
        print("\nSample ticket data:")
        print(tickets_df.head())

    ##USERS
    print("\n4. USERS:")
    print("-" * 40)
    users_df = get_all_users()
    print(f"Users count: {len(users_df)}")
    test_username = "test_crud_user"
    if check_username_exists(test_username):
        delete_user(test_username)

    test_password_hash = "$2b$12$TestHash123"
    user_id = insert_user(test_username, test_password_hash, "tester")
    if user_id:
        print(f"Created user #{user_id}")

    users_df = get_all_users()
    print(f"Total users: {len(users_df)}")

    # 5. cleaning data
    print("\n" + "-" * 30)
    print("CLEANUP")
    print("-" * 30)

    if  incident_id:
        delete_incident(incident_id)
        print(f"Deleted incident #{incident_id}")

    if test_ticket_id:
        delete_ticket(test_ticket_id)
        print(f"Deleted ticket #{test_ticket_id}")

    if dataset_id:
        delete_dataset(dataset_id)
        print(f"Deleted dataset #{dataset_id}")

    if test_username:
        delete_user(test_username)
        print(f"Deleted user '{test_username}'")

def demonstrate_all_crud():
    """Show CRUD for all 3 domains """
    print("\n" + "=" * 60)
    print("DEMONSTRATING CRUD FOR ALL 3 DOMAINS")
    print("=" * 60)

    # 1. CYBERSECURITY DOMAIN
    print("\n1. CYBERSECURITY:")
    print("   Create: Insert new incident")
    incident_id = insert_incident("2024-11-10", "DDoS", "High", "Open", "Test DDoS attack", "admin")
    print(f"   Create: Incident #{incident_id}")
    incidents = get_all_incidents()
    print(f"   Read: {len(incidents)} incidents")
    conn = connect_database()
    if incident_id:
        update_incident_status(conn, incident_id, "In Progress")
        print("   Update: Status changed")
        delete_incident(conn, incident_id)
        print("   Delete: Incident removed")
    conn.close()

    # 2. DATA SCIENCE DOMAIN
    print("\n2. DATA SCIENCE:")
    print("   Create: Insert new dataset")
    dataset_id = insert_dataset("Test_Dataset", "Test", "Manual", "2024-11-10", 100, 5.0, "admin", "2024-11-10")
    print(f"   Created dataset #{dataset_id}")
    datasets = get_all_datasets()
    print(f"   Read: {len(datasets)} datasets")

    if dataset_id:
        update_dataset_record_count(dataset_id, 750)
        print("   Update: Record count updated")
        delete_dataset(dataset_id)
        print("   Delete: Dataset removed")
    conn.close()

    # 3. IT OPERATIONS DOMAIN
    print("\n3. IT OPERATIONS:")
    print("   Create: Insert new ticket")
    demo_ticket_id = "TDEMO001"
    ticket_id = insert_ticket(demo_ticket_id, "Medium", "Test Ticket", "Testing CRUD", "IT_Support_A", "General", "Open", None)
    print(f"Created ticket #{ticket_id}")
    tickets = get_all_tickets()
    print(f"   Read: {len(tickets)} tickets")

    if demo_ticket_id:
        update_ticket_status(demo_ticket_id, "Resolved")
        print("   Update: Status updated")
        delete_ticket(demo_ticket_id)
        print(" Delete: Ticket removed")
    conn.close()

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
    total_rows = load_all_csv_data(conn, csv_paths_map)
    print(f"Loaded {total_rows} rows")

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
