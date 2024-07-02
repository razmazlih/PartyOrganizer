import datetime
from typing import List, Union
from dataclasses import dataclass
import os
from json import loads, dumps

MY_DATA_FILE = os.path.join(os.path.dirname(os.getcwd()), "data", "my_text.json")

def _save_in_file(data_to_save):
    with open(MY_DATA_FILE, "w") as file:
        file.write(dumps(data_to_save))

def _load_from_file():
    with open(MY_DATA_FILE, "r") as file:
        return loads(file.read())

@dataclass
class Guest:
    name: str
    id_number: int
    entered: bool = False
    confirmed: bool = False

    def __repr__(self) -> str:
        return f"Guest(name={self.name}, id_number={self.id_number}, entered={self.entered}, confirmed={self.confirmed})"

class Group:
    def __init__(self, name: str):
        self.name = name
        self.guests = {}

    def add_guest(self, guest: Guest) -> str:
        if guest.id_number in self.guests:
            return f"Guest {guest.name} is already in the group {self.name}"
        self.guests[guest.id_number] = guest
        return f"Guest {guest.name} added to group {self.name}"

    def list_guests(self) -> List[Guest]:
        return list(self.guests.values())

    def __repr__(self) -> str:
        return f"Group(name={self.name}, guests={list(self.guests.values())})"

class PartyOrganizer:
    def __init__(self):
        self.guests = {}
        self.groups = {}
        self.party_date = None

    @staticmethod
    def _valid_id(id_number: str) -> bool:
        """
        בודק אם מספר תעודת הזהות תקין (9 ספרות).
        """
        return len(id_number) == 9 and id_number.isdigit()

    def set_party_date(self, date_str: str) -> str:
        """
        קובע את תאריך המסיבה.
        קלט: מחרוזת תאריך בפורמט YYYY-MM-DD HH:MM
        """
        try:
            self.party_date = datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M')
            return f"Party date set to {self.party_date}"
        except ValueError:
            return "Invalid date format. Please use YYYY-MM-DD HH:MM."

    def add_guest(self, name: str, id_number: str) -> str:
        """
        מוסיף אורח חדש לרשימה.
        קלט: שם, מספר תעודת זהות
        """
        if not self._valid_id(id_number):
            return "Id number isn't valid"

        guest_id = int(id_number)
        if guest_id in self.guests:
            return f"Id {id_number} is already in the system"

        if len(name) < 2:
            return f"\"{name}\" is too short (minimum 2 letters)"

        guest = Guest(name, guest_id)
        self.guests[guest_id] = guest
        return f"Guest {name} added."

    def mark_as_entered(self, id_number: str) -> str:
        """
        מסמן אורח כמי שנכנס לאירוע.
        קלט: מספר תעודת זהות
        """
        if not self._valid_id(id_number):
            return "Id number isn't valid"

        guest_id = int(id_number)
        if guest_id in self.guests:
            self.guests[guest_id].entered = True
            return f"Guest {self.guests[guest_id].name} entered."
        return f"No guest found with id {id_number}."

    def confirm_attendance(self, id_number: str) -> str:
        """
        מאשר השתתפות של אורח.
        קלט: מספר תעודת זהות
        """
        if not self._valid_id(id_number):
            return "Id number isn't valid"

        guest_id = int(id_number)
        if guest_id in self.guests:
            self.guests[guest_id].confirmed = True
            return f"Guest {self.guests[guest_id].name} confirmed attendance."
        return f"No guest found with id {id_number}."

    def list_guests(self) -> str:
        """
        מציג את רשימת האורחים עם סטטוס כניסה ואישור.
        """
        return "\n".join(
            f"{guest.name} ({guest.id_number}) - {'Entered' if guest.entered else 'Not entered'}, {'Confirmed' if guest.confirmed else 'Not confirmed'}"
            for guest in self.guests.values()
        )

    def list_entered_guests(self) -> List[Guest]:
        """
        מציג את רשימת האורחים שנכנסו לאירוע.
        """
        return [guest for guest in self.guests.values() if guest.entered]

    def list_not_entered_guests(self) -> List[Guest]:
        """
        מציג את רשימת האורחים שלא נכנסו לאירוע.
        """
        return [guest for guest in self.guests.values() if not guest.entered]

    def remove_guest(self, id_number: str) -> str:
        """
        מסיר אורח מהרשימה.
        קלט: מספר תעודת זהות
        """
        if not self._valid_id(id_number):
            return "Id number isn't valid"

        guest_id = int(id_number)
        if guest_id in self.guests:
            removed_guest = self.guests.pop(guest_id)
            return f"Guest {removed_guest.name} removed."
        return f"No guest found with id {id_number}."

    def find_guest(self, id_number: str) -> Union[Guest, str]:
        """
        מוצא אורח לפי מספר תעודת זהות.
        קלט: מספר תעודת זהות
        """
        if not self._valid_id(id_number):
            return "Id number isn't valid"

        guest_id = int(id_number)
        return self.guests.get(guest_id, f"No guest found with id {id_number}.")

    def generate_report(self) -> str:
        """
        יוצר דו"ח סטטיסטיקות על האורחים.
        """
        total_guests = len(self.guests)
        entered_guests = len(self.list_entered_guests())
        not_entered_guests = len(self.list_not_entered_guests())

        return (
            f"Total guests: {total_guests}\n"
            f"Entered guests: {entered_guests}\n"
            f"Not entered guests: {not_entered_guests}"
        )

    def add_group(self, group_name: str) -> str:
        """
        יוצר קבוצה חדשה.
        קלט: שם קבוצה
        """
        if group_name in self.groups:
            return f"Group {group_name} already exists."
        self.groups[group_name] = Group(group_name)
        return f"Group {group_name} created."

    def add_guest_to_group(self, id_number: str, group_name: str) -> str:
        """
        מוסיף אורח לקבוצה מסוימת.
        קלט: מספר תעודת זהות, שם קבוצה
        """
        if not self._valid_id(id_number):
            return "Id number isn't valid"

        guest_id = int(id_number)
        if guest_id not in self.guests:
            return "Guest not found"

        if group_name not in self.groups:
            return f"Group {group_name} does not exist. Please create the group first."

        guest = self.guests[guest_id]
        return self.groups[group_name].add_guest(guest)

    def list_group_guests(self, group_name: str) -> Union[str, List[Guest]]:
        """
        מציג את רשימת האורחים בקבוצה מסוימת.
        קלט: שם קבוצה
        """
        if group_name in self.groups:
            return self.groups[group_name].list_guests()
        return f"No group found with name {group_name}."
