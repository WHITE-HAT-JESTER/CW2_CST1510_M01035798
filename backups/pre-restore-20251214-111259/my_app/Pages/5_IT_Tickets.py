import streamlit as st
import pandas as pd
from datetime import datetime
from my_app.data.tickets import get_all_tickets, insert_ticket

st.title("IT Operations")

# Get existing tickets
tickets_df = get_all_tickets()

# Show existing tickets
st.subheader("Existing Tickets")
if tickets_df.empty:
    st.info("No tickets yet. Create one below!")
else:
    st.dataframe(tickets_df)

# Add new ticket form
st.subheader("Create New Ticket")
with st.form("add_ticket"):
    ticket_id = st.text_input("Ticket ID (e.g., T001)")
    subject = st.text_input("Subject")
    description = st.text_area("Description")
    priority = st.selectbox("Priority", ["Low", "Medium", "High"])
    category = st.selectbox("Category", ["Hardware", "Software", "Network", "General"])
    assigned_to = st.text_input("Assign to")

    submitted = st.form_submit_button("Create Ticket")

    if submitted:
        if ticket_id and subject and description and assigned_to:
            # Add ticket
            result = insert_ticket(
                ticket_id=ticket_id,
                priority=priority,
                subject=subject,
                description=description,
                assigned_to=assigned_to,
                category=category,
                status="Open",
                resolved_date=None,
                created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )

            if result:
                st.success("Ticket created successfully!")
                st.rerun()
            else:
                st.error("Could not create ticket. Check if ID is unique.")
        else:
            st.warning("Please fill in all fields.")