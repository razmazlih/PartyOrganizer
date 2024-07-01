import streamlit as st
from logic.data_managment import PartyOrganizer

organizer = PartyOrganizer()

st.title('Party Organizer')

# Add Guest
st.header('Add Guest')
name = st.text_input('Name')
id_number = st.text_input('ID Number')
if st.button('Add Guest'):
    message = organizer.add_guest(name, id_number)
    print(organizer.list_guests())
    st.write(message)

# Mark Entered
st.header('Mark Entered')
enter_id = st.text_input('ID Number to Mark Entered')
if st.button('Mark Entered'):
    message = organizer.mark_as_entered(enter_id)
    st.write(message)

# Confirm Attendance
st.header('Confirm Attendance')
confirm_id = st.text_input('ID Number to Confirm Attendance')
if st.button('Confirm Attendance'):
    message = organizer.confirm_attendance(confirm_id)
    st.write(message)

# List Guests
st.header('Guests List')
if st.button('Show Guests'):
    st.text(organizer.list_guests())

# Generate Report
st.header('Report')
if st.button('Generate Report'):
    report = organizer.generate_report()
    st.text(report)