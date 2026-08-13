"""
ticket_service.py
Core business logic for the IT Helpdesk system: creating tickets,
assigning technicians, adding troubleshooting notes, escalating,
and resolving tickets.
"""

from datetime import datetime
from app.database import get_connection
from app.priority import calculate_priority

VALID_STATUSES = ("Open", "In Progress", "Escalated", "Resolved", "Closed")


def _now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def create_ticket(user_id, title, description, type_, category, impact, urgency):
    """Create a new ticket. Priority is derived automatically from impact/urgency."""
    priority = calculate_priority(impact, urgency)
    conn = get_connection()
    cur = conn.execute(
        """INSERT INTO tickets
           (user_id, title, description, type, category, impact, urgency,
            priority, status, assigned_to, created_at, resolved_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'Open', NULL, ?, NULL)""",
        (user_id, title, description, type_, category, impact, urgency, priority, _now()),
    )
    conn.commit()
    ticket_id = cur.lastrowid
    conn.close()
    return ticket_id, priority


def get_ticket(ticket_id):
    conn = get_connection()
    row = conn.execute("SELECT * FROM tickets WHERE id = ?", (ticket_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def list_open_tickets():
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM tickets WHERE status NOT IN ('Resolved', 'Closed') "
        "ORDER BY CASE priority "
        "  WHEN 'Critical' THEN 1 WHEN 'High' THEN 2 "
        "  WHEN 'Medium' THEN 3 ELSE 4 END, created_at"
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def list_all_tickets():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM tickets ORDER BY id").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def assign_technician(ticket_id, technician_id):
    conn = get_connection()
    conn.execute(
        "UPDATE tickets SET assigned_to = ?, status = 'In Progress' WHERE id = ?",
        (technician_id, ticket_id),
    )
    conn.execute(
        "INSERT INTO ticket_updates (ticket_id, technician_id, note, created_at) "
        "VALUES (?, ?, ?, ?)",
        (ticket_id, technician_id, "Ticket assigned to technician.", _now()),
    )
    conn.commit()
    conn.close()


def add_note(ticket_id, technician_id, note):
    """Add a troubleshooting note / ticket update."""
    conn = get_connection()
    conn.execute(
        "INSERT INTO ticket_updates (ticket_id, technician_id, note, created_at) "
        "VALUES (?, ?, ?, ?)",
        (ticket_id, technician_id, note, _now()),
    )
    conn.commit()
    conn.close()


def update_status(ticket_id, status):
    if status not in VALID_STATUSES:
        raise ValueError(f"Invalid status: {status}. Must be one of {VALID_STATUSES}")
    conn = get_connection()
    resolved_at = _now() if status in ("Resolved", "Closed") else None
    if resolved_at:
        conn.execute(
            "UPDATE tickets SET status = ?, resolved_at = ? WHERE id = ?",
            (status, resolved_at, ticket_id),
        )
    else:
        conn.execute("UPDATE tickets SET status = ? WHERE id = ?", (status, ticket_id))
    conn.execute(
        "INSERT INTO ticket_updates (ticket_id, technician_id, note, created_at) "
        "VALUES (?, NULL, ?, ?)",
        (ticket_id, f"Status changed to '{status}'.", _now()),
    )
    conn.commit()
    conn.close()


def escalate_ticket(ticket_id, reason):
    """Escalate a ticket: mark status Escalated and log the reason."""
    conn = get_connection()
    conn.execute("UPDATE tickets SET status = 'Escalated' WHERE id = ?", (ticket_id,))
    conn.execute(
        "INSERT INTO ticket_updates (ticket_id, technician_id, note, created_at) "
        "VALUES (?, NULL, ?, ?)",
        (ticket_id, f"Escalated: {reason}", _now()),
    )
    conn.commit()
    conn.close()


def resolve_ticket(ticket_id, resolution_note):
    """Resolve a ticket and log the resolution note."""
    add_note(ticket_id, None, f"Resolution: {resolution_note}")
    update_status(ticket_id, "Resolved")


def get_ticket_history(ticket_id):
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM ticket_updates WHERE ticket_id = ? ORDER BY id", (ticket_id,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def list_technicians():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM technicians ORDER BY id").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def list_users():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM users ORDER BY id").fetchall()
    conn.close()
    return [dict(r) for r in rows]
