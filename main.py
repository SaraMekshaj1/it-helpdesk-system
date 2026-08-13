"""
main.py
Command-line interface for the IT Helpdesk & Ticket Management System.

Run with: python main.py
"""

import os
from app.database import init_db, DB_PATH
from app import ticket_service as svc

IMPACT_URGENCY_OPTIONS = {"1": "Low", "2": "Medium", "3": "High"}
TYPE_OPTIONS = {"1": "Incident", "2": "Service Request"}


def pause():
    input("\nPress Enter to continue...")


def print_header():
    print("=" * 35)
    print("       IT HELPDESK SYSTEM")
    print("=" * 35)


def choose(prompt, options: dict):
    print(prompt)
    for key, label in options.items():
        print(f"{key}. {label}")
    while True:
        choice = input("Choose: ").strip()
        if choice in options:
            return options[choice]
        print("Invalid choice, try again.")


def print_ticket_row(t):
    print(f"#{t['id']:<4} [{t['priority']:<8}] {t['status']:<12} {t['title']}")


def action_create_ticket():
    print("\nCreate Ticket\n")
    users = svc.list_users()
    if not users:
        print("No users found. Please seed the database first.")
        return
    for u in users:
        print(f"{u['id']}. {u['name']}")
    user_id = int(input("User ID: ").strip())

    title = input("Title: ").strip()
    description = input("Description: ").strip()
    category = input("Category (e.g. Network, Email, Hardware, Security, Access Management): ").strip()

    print()
    type_ = choose("Type:", TYPE_OPTIONS)
    print()
    impact = choose("Impact:", IMPACT_URGENCY_OPTIONS)
    print()
    urgency = choose("Urgency:", IMPACT_URGENCY_OPTIONS)

    ticket_id, priority = svc.create_ticket(user_id, title, description, type_, category, impact, urgency)

    print("\nTicket created successfully!\n")
    print(f"Ticket ID: #{ticket_id}")
    print(f"Priority: {priority}")
    print("Status: Open")


def action_view_open():
    print("\nOpen Tickets\n")
    tickets = svc.list_open_tickets()
    if not tickets:
        print("No open tickets.")
        return
    for t in tickets:
        print_ticket_row(t)


def action_update_ticket():
    print("\nUpdate Ticket\n")
    ticket_id = int(input("Ticket ID: ").strip())
    t = svc.get_ticket(ticket_id)
    if not t:
        print("Ticket not found.")
        return
    note = input("Troubleshooting note to add: ").strip()
    techs = svc.list_technicians()
    tech_id = None
    if techs:
        print("Technicians:")
        for tech in techs:
            print(f"{tech['id']}. {tech['name']} ({tech['level']})")
        raw = input("Technician ID (leave blank for none): ").strip()
        tech_id = int(raw) if raw else None
    svc.add_note(ticket_id, tech_id, note)

    status = choose(
        "\nUpdate status?",
        {"1": "Open", "2": "In Progress", "3": "Escalated", "4": "Resolved", "5": "Closed", "6": "No change"},
    )
    if status != "No change":
        svc.update_status(ticket_id, status)
    print("\nTicket updated.")


def action_assign_technician():
    print("\nAssign Technician\n")
    ticket_id = int(input("Ticket ID: ").strip())
    techs = svc.list_technicians()
    if not techs:
        print("No technicians found.")
        return
    for tech in techs:
        print(f"{tech['id']}. {tech['name']} ({tech['level']})")
    tech_id = int(input("Technician ID: ").strip())
    svc.assign_technician(ticket_id, tech_id)
    print("\nTechnician assigned. Status set to 'In Progress'.")


def action_escalate():
    print("\nEscalate Ticket\n")
    ticket_id = int(input("Ticket ID: ").strip())
    reason = input("Escalation reason: ").strip()
    svc.escalate_ticket(ticket_id, reason)
    print("\nTicket escalated.")


def action_resolve():
    print("\nResolve Ticket\n")
    ticket_id = int(input("Ticket ID: ").strip())
    resolution = input("Resolution summary: ").strip()
    svc.resolve_ticket(ticket_id, resolution)
    print("\nTicket resolved.")


def action_history():
    print("\nTicket History\n")
    ticket_id = int(input("Ticket ID: ").strip())
    t = svc.get_ticket(ticket_id)
    if not t:
        print("Ticket not found.")
        return
    print(f"\nTicket #{t['id']}: {t['title']}")
    print(f"Type: {t['type']} | Category: {t['category']}")
    print(f"Impact: {t['impact']} | Urgency: {t['urgency']} | Priority: {t['priority']}")
    print(f"Status: {t['status']}")
    print(f"Created: {t['created_at']} | Resolved: {t['resolved_at'] or '-'}")
    print("\nUpdates:")
    for u in svc.get_ticket_history(ticket_id):
        who = f"tech#{u['technician_id']}" if u['technician_id'] else "system"
        print(f"  [{u['created_at']}] ({who}) {u['note']}")


MENU = {
    "1": ("Create ticket", action_create_ticket),
    "2": ("View open tickets", action_view_open),
    "3": ("Update ticket", action_update_ticket),
    "4": ("Assign technician", action_assign_technician),
    "5": ("Escalate ticket", action_escalate),
    "6": ("Resolve ticket", action_resolve),
    "7": ("View ticket history", action_history),
}


def main():
    if not os.path.exists(DB_PATH):
        init_db()

    while True:
        print()
        print_header()
        print()
        for key, (label, _) in MENU.items():
            print(f"{key}. {label}")
        print("0. Exit")
        print()
        choice = input("Choose: ").strip()

        if choice == "0":
            print("Goodbye!")
            break
        elif choice in MENU:
            try:
                MENU[choice][1]()
            except Exception as e:
                print(f"\nError: {e}")
            pause()
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
