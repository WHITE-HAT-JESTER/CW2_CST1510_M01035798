import streamlit as st
import pandas as pd
from datetime import datetime
from my_app.data.incidents import get_all_incidents, insert_incident

df_incidents=get_all_incidents()
st.dataframe(df_incidents)
st.subheader("Cyber Incidents")

df_incidents = get_all_incidents()

if df_incidents.empty:
    st.info("No incidents in database yet. Add one below!")
else:
    # Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Incidents", len(df_incidents))
    with col2:
        st.metric("High/Critical", len(df_incidents[df_incidents["severity"].isin(["High", "Critical"])]))
    with col3:
        st.metric("Open", len(df_incidents[df_incidents["status"] == "Open"]))

    # Bar chart
    severity_counts = df_incidents["severity"].value_counts()
    st.bar_chart(severity_counts)

    # Show table
    st.dataframe(df_incidents, width=True)

# New Incident Form
st.markdown("## New Incident")

with st.form("incident_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        date = st.date_input("Date of Incident", value=datetime.today())
        incident_type = st.selectbox("Type", ["Phishing", "Malware", "DDoS", "Brute Force", "Data Leak", "Insider Threat"])
    with col2:
        severity = st.selectbox("Severity", ["Low", "Medium", "High", "Critical"])
        status = st.selectbox("Status", ["Open", "In Progress", "Resolved", "Closed"])

    description = st.text_area("Description")
    reported_by = st.text_input("Reported by (your name)", value="admin")

    submitted = st.form_submit_button("Submit Incident", type="primary")

    if submitted:

        insert_incident(
            date=str(date),
            incident_type=incident_type,
            severity=severity,
            status=status,
            description=description,
            reported_by=reported_by
        )
        st.success(f"Incident reported on {date}!")
        st.rerun()



