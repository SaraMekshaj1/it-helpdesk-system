"""
seed.py
Populates the database with realistic demo data: departments, users,
technicians, and a set of tickets covering common IT support scenarios
(account/access issues, email problems, security incidents, and
service requests).

Run with: python -m app.seed
"""

from datetime import datetime
from app.database import reset_db, get_connection
from app.ticket_service import create_ticket, assign_technician, add_note, resolve_ticket, escalate_ticket, update_status


def seed():
    reset_db()
    conn = get_connection()

    # --- Departments ---
    departments = ["Finance", "Human Resources", "Sales", "Engineering", "Marketing"]
    dept_ids = {}
    for d in departments:
        cur = conn.execute("INSERT INTO departments (name) VALUES (?)", (d,))
        dept_ids[d] = cur.lastrowid

    # --- Users ---
    users = [
        ("John Smith", "john.smith@company.com", "Finance"),
        ("Maria Garcia", "maria.garcia@company.com", "Human Resources"),
        ("Alex Chen", "alex.chen@company.com", "Sales"),
        ("Priya Patel", "priya.patel@company.com", "Engineering"),
        ("Tom Becker", "tom.becker@company.com", "Marketing"),
        ("Elena Rossi", "elena.rossi@company.com", "Finance"),
    ]
    user_ids = {}
    for name, email, dept in users:
        cur = conn.execute(
            "INSERT INTO users (name, email, department_id) VALUES (?, ?, ?)",
            (name, email, dept_ids[dept]),
        )
        user_ids[name] = cur.lastrowid

    # --- Technicians ---
    technicians = [("Sam Osei", "L1"), ("Nina Kowalski", "L2"), ("David Lee", "L3")]
    tech_ids = {}
    for name, level in technicians:
        cur = conn.execute("INSERT INTO technicians (name, level) VALUES (?, ?)", (name, level))
        tech_ids[name] = cur.lastrowid

    conn.commit()
    conn.close()

    # --- Tickets: realistic scenarios ---

    # 1. Incident: cannot access internal application (Network / DNS)
    tid, _ = create_ticket(
        user_ids["John Smith"], "Cannot access internal application",
        "User reports the internal finance application is unreachable from their workstation.",
        "Incident", "Network", "High", "High"
    )
    assign_technician(tid, tech_ids["David Lee"])
    add_note(tid, tech_ids["David Lee"], "Verified network connectivity - OK.")
    add_note(tid, tech_ids["David Lee"], "Checked DNS resolution - stale record found.")
    add_note(tid, tech_ids["David Lee"], "Tested application server - responding normally.")
    add_note(tid, tech_ids["David Lee"], "Checked user permissions - correct.")
    resolve_ticket(tid, "DNS configuration corrected.")

    # 2. Incident: cannot access shared Finance folder (permissions)
    tid, _ = create_ticket(
        user_ids["Elena Rossi"], "Cannot access shared Finance folder",
        "User is unable to open the shared Finance drive after a recent reorganization.",
        "Incident", "Access Management", "Medium", "High"
    )
    assign_technician(tid, tech_ids["Nina Kowalski"])
    add_note(tid, tech_ids["Nina Kowalski"], "Checked network connectivity - OK.")
    add_note(tid, tech_ids["Nina Kowalski"], "Verified user account - active, no lockout.")
    add_note(tid, tech_ids["Nina Kowalski"], "Checked security group membership - user missing from Finance-ReadWrite group.")
    add_note(tid, tech_ids["Nina Kowalski"], "Identified missing group membership as root cause.")
    add_note(tid, tech_ids["Nina Kowalski"], "Added user to authorized security group.")
    add_note(tid, tech_ids["Nina Kowalski"], "Verified access restored.")
    resolve_ticket(tid, "User added to correct security group; access confirmed.")

    # 3. Incident: employee cannot send email
    tid, _ = create_ticket(
        user_ids["Tom Becker"], "Employee cannot send email",
        "User can receive but not send emails since this morning.",
        "Incident", "Email", "Medium", "Medium"
    )
    assign_technician(tid, tech_ids["Sam Osei"])
    add_note(tid, tech_ids["Sam Osei"], "Checked internet connectivity - OK.")
    add_note(tid, tech_ids["Sam Osei"], "Verified account access - login successful.")
    add_note(tid, tech_ids["Sam Osei"], "Checked mailbox status - mailbox near storage quota.")
    add_note(tid, tech_ids["Sam Osei"], "Confirmed issue is not recipient-specific.")
    add_note(tid, tech_ids["Sam Osei"], "Checked attachment size on failed messages - within limits.")
    add_note(tid, tech_ids["Sam Osei"], "Root cause: mailbox storage quota exceeded, blocking outbound mail.")
    resolve_ticket(tid, "Archived old items and increased mailbox quota; outbound mail restored.")

    # 4. Security incident: phishing link clicked
    tid, _ = create_ticket(
        user_ids["Maria Garcia"], "Employee clicked suspicious phishing link",
        "User reports clicking a link in a suspicious email requesting credential re-entry.",
        "Incident", "Security", "High", "High"
    )
    add_note(tid, None, "User reported the incident immediately via the security hotline.")
    add_note(tid, None, "User instructed not to interact further with the email or enter any credentials.")
    escalate_ticket(tid, "Potential credential compromise - escalated to security team per incident response procedure.")
    assign_technician(tid, tech_ids["David Lee"])
    add_note(tid, tech_ids["David Lee"], "Account and active sessions reviewed according to security procedure.")
    add_note(tid, tech_ids["David Lee"], "No signs of unauthorized access found; password reset enforced as a precaution.")
    resolve_ticket(tid, "Password reset enforced, sessions revoked, user re-briefed on phishing awareness.")

    # 5. Service Request: access to HR application
    tid, _ = create_ticket(
        user_ids["Alex Chen"], "Request for access to HR application",
        "New team lead requires read access to the HR reporting application for headcount planning.",
        "Service Request", "Access Management", "Low", "Medium"
    )
    add_note(tid, None, "Request submitted and pending manager authorization.")
    add_note(tid, None, "Authorization received from department manager.")
    assign_technician(tid, tech_ids["Sam Osei"])
    add_note(tid, tech_ids["Sam Osei"], "Added user to HR-ReportingReadOnly group membership.")
    add_note(tid, tech_ids["Sam Osei"], "Access granted; verified user can log in and view reports.")
    resolve_ticket(tid, "Access granted and verified. Request closed.")

    # 6. Incident: printer not working (kept open, in progress)
    tid, _ = create_ticket(
        user_ids["Priya Patel"], "Printer not working",
        "Office printer on the 3rd floor is showing a paper jam error that will not clear.",
        "Incident", "Hardware", "Low", "Low"
    )
    assign_technician(tid, tech_ids["Sam Osei"])
    add_note(tid, tech_ids["Sam Osei"], "Checked printer for visible paper jam - cleared jammed sheet.")
    update_status(tid, "In Progress")
    add_note(tid, tech_ids["Sam Osei"], "Printer still shows error after reboot; ordering replacement roller kit.")

    # 7. Service Request: new laptop setup (still open)
    tid, _ = create_ticket(
        user_ids["Elena Rossi"], "New laptop setup for onboarding employee",
        "New hire starts Monday and needs a laptop imaged with standard Finance software.",
        "Service Request", "Hardware Provisioning", "Low", "Medium"
    )
    add_note(tid, None, "Request logged; laptop reserved from stock.")

    # 8. Incident: VPN connection drops intermittently (escalated, in progress)
    tid, _ = create_ticket(
        user_ids["Tom Becker"], "VPN connection drops intermittently",
        "User working remotely reports VPN disconnects every 10-15 minutes, disrupting video calls.",
        "Incident", "Network", "Medium", "High"
    )
    assign_technician(tid, tech_ids["Nina Kowalski"])
    add_note(tid, tech_ids["Nina Kowalski"], "Checked VPN client version - up to date.")
    add_note(tid, tech_ids["Nina Kowalski"], "Reviewed VPN server logs - repeated re-authentication events for this user.")
    escalate_ticket(tid, "Suspected VPN concentrator issue affecting multiple remote users - escalated to network team.")

    # 9. Incident: application crashes on launch
    tid, _ = create_ticket(
        user_ids["Priya Patel"], "CRM application crashes on launch",
        "CRM desktop client crashes immediately after login on user's workstation.",
        "Incident", "Software", "Medium", "Medium"
    )
    assign_technician(tid, tech_ids["Nina Kowalski"])
    add_note(tid, tech_ids["Nina Kowalski"], "Reviewed crash logs - corrupted local cache identified.")
    add_note(tid, tech_ids["Nina Kowalski"], "Cleared local application cache and reinstalled client.")
    resolve_ticket(tid, "Application reinstalled with clean cache; confirmed working by user.")

    # 10. Service Request: software license request
    tid, _ = create_ticket(
        user_ids["Alex Chen"], "Request for additional Excel add-in license",
        "Sales analyst needs a licensed data-analysis add-in for quarterly forecasting.",
        "Service Request", "Software Licensing", "Low", "Low"
    )
    add_note(tid, None, "Request submitted; checking available license pool.")
    assign_technician(tid, tech_ids["Sam Osei"])
    add_note(tid, tech_ids["Sam Osei"], "License available in pool; assigned to user's account.")
    resolve_ticket(tid, "License assigned and installed; user confirmed functionality.")

    print("Database seeded successfully with 10 realistic tickets.")


if __name__ == "__main__":
    seed()
