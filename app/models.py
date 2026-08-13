"""
models.py
Lightweight dataclasses representing the core entities of the system.
These mirror the SQLite schema and are used to pass data around cleanly.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Department:
    id: Optional[int]
    name: str


@dataclass
class User:
    id: Optional[int]
    name: str
    email: str
    department_id: Optional[int]


@dataclass
class Technician:
    id: Optional[int]
    name: str
    level: str  # 'L1', 'L2', 'L3'


@dataclass
class Ticket:
    id: Optional[int]
    user_id: int
    title: str
    description: str
    type: str          # 'Incident' or 'Service Request'
    category: str
    impact: str         # 'Low' | 'Medium' | 'High'
    urgency: str         # 'Low' | 'Medium' | 'High'
    priority: str        # 'Low' | 'Medium' | 'High' | 'Critical'
    status: str            # 'Open' | 'In Progress' | 'Escalated' | 'Resolved' | 'Closed'
    assigned_to: Optional[int]
    created_at: str
    resolved_at: Optional[str]


@dataclass
class TicketUpdate:
    id: Optional[int]
    ticket_id: int
    technician_id: Optional[int]
    note: str
    created_at: str
