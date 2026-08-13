# IT Helpdesk & Ticket Management System

A Python + SQLite application that simulates an internal IT helpdesk: users submit
incidents and service requests, priority is calculated automatically from
impact and urgency, technicians work tickets through a realistic lifecycle
(assign → troubleshoot → escalate if needed → resolve), and every action is
logged as an auditable ticket update.

Built to demonstrate core IT support / ITSM concepts: incident vs. service
request handling, impact/urgency-based prioritization, troubleshooting
documentation, escalation workflows, and relational data modeling with SQL.

## Why this project

Most beginner CRUD apps just store and display records. This one models how
an actual IT helpdesk operates:

- Tickets are classified as **Incidents** (something broken) or **Service
  Requests** (something requested).
- **Priority** is derived automatically from Impact + Urgency, using a matrix
  inspired by common ITIL practice — not just picked manually.
- Every ticket keeps a full **audit trail** (`ticket_updates`) of
  troubleshooting steps, assignments, escalations, and resolutions.
- The seed data reflects **real support scenarios** (DNS issues, permission
  problems, mailbox quota errors, a phishing incident with proper escalation,
  and access-request workflows) rather than generic placeholder text.

## Ticket Lifecycle

```
Create Ticket
      ↓
Incident or Service Request
      ↓
Set Impact / Set Urgency
      ↓
Calculate Priority (auto)
      ↓
Assign Technician
      ↓
Update Status
      ↓
Add Troubleshooting Notes
      ↓
Escalate if necessary
      ↓
Resolve
```

## Priority Matrix

Priority is calculated using a simple impact/urgency matrix inspired by
common IT service management practices. In a real organization, the exact
matrix would follow the organization's policies.

| Impact | Urgency | Priority |
|--------|---------|----------|
| High   | High    | Critical |
| High   | Medium  | High     |
| Medium | High    | High     |
| Medium | Medium  | Medium   |
| High   | Low     | Medium   |
| Low    | High    | Medium   |
| Medium | Low     | Low      |
| Low    | Medium  | Low      |
| Low    | Low     | Low      |

Implemented as a pure, unit-tested function in [`app/priority.py`](app/priority.py)
so it can be reused independently of the CLI or database layer.

## Data Model

SQLite database with five related tables:

```
departments        users               technicians
----------          ----------           ----------
id                  id                  id
name                name                name
                    email               level (L1/L2/L3)
                    department_id


tickets                              ticket_updates
----------                            ----------
id                                    id
user_id            -> users.id        ticket_id      -> tickets.id
title                                 technician_id  -> technicians.id
description                           note
type        (Incident / Service Req)  created_at
category
impact      (Low / Medium / High)
urgency     (Low / Medium / High)
priority    (Low / Medium / High / Critical)
status      (Open / In Progress / Escalated / Resolved / Closed)
assigned_to        -> technicians.id
created_at
resolved_at
```

## Example Ticket

```
Ticket #1

User:            John Smith
Department:      Finance
Type:             Incident
Category:         Network
Description:      Cannot access the internal application.

Impact:            High
Urgency:           High
Priority:          Critical

Status:            Resolved

Troubleshooting:
 - Verified network connectivity
 - Checked DNS resolution - stale record found
 - Tested application server - responding normally
 - Checked user permissions - correct

Resolution:
 DNS configuration corrected.
```

## Realistic Scenarios Included

The seed script ([`app/seed.py`](app/seed.py)) loads 10 tickets covering:

- **Network/DNS incident** — internal app unreachable, traced to a stale DNS record.
- **Access/permissions incident** — shared drive access lost after a security group change.
- **Email incident** — outbound mail blocked by a mailbox storage quota.
- **Security incident** — employee clicked a phishing link; ticket is escalated
  to the security team, account/session reviewed, password reset enforced.
- **Service request** — new access to the HR application, following an
  authorization → provisioning → verification workflow.
- **Hardware incident** — printer fault, left in progress with a parts order note.
- **Provisioning request** — new-hire laptop setup, left open.
- **Network incident** — intermittent VPN drops, escalated to the network team.
- **Software incident** — CRM crash traced to a corrupted local cache.
- **Licensing request** — software add-in license assigned from pool.

This mix intentionally includes resolved, in-progress, escalated, and open
tickets so the system demonstrates the full lifecycle, not just the happy path.

## CLI

A deliberately simple command-line interface — no web framework, no auth,
no Docker — so all the effort goes into the domain logic and data model.

```
===================================
       IT HELPDESK SYSTEM
===================================

1. Create ticket
2. View open tickets
3. Update ticket
4. Assign technician
5. Escalate ticket
6. Resolve ticket
7. View ticket history
0. Exit

Choose: 2

Open Tickets

#8    [High    ] Escalated    VPN connection drops intermittently
#6    [Low     ] In Progress  Printer not working
#7    [Low     ] Open         New laptop setup for onboarding employee
```

Creating a ticket:

```
Create Ticket

Title: Printer not working
Type:
1. Incident
2. Service Request
Choose: 1

Impact:
1. Low
2. Medium
3. High
Choose: 1

Urgency:
1. Low
2. Medium
3. High
Choose: 1

Ticket created successfully!

Ticket ID: #11
Priority: Low
Status: Open
```

## Project Structure

```
it-helpdesk-system/
│
├── app/
│   ├── database.py       # SQLite connection + schema
│   ├── models.py         # Dataclasses mirroring the schema
│   ├── ticket_service.py # Core business logic (create/assign/escalate/resolve)
│   ├── priority.py       # Impact/urgency -> priority matrix
│   └── seed.py            # Realistic demo data
│
├── tests/
│   └── test_priority.py  # Unit tests for the priority matrix
│
├── screenshots/
├── README.md
├── requirements.txt
└── main.py                # CLI entry point
```

## Getting Started

```bash
# 1. Clone the repository
git clone https://github.com/SaraMekshaj1/it-helpdesk-system.git
cd it-helpdesk-system

# 2. Install dependencies
pip install -r requirements.txt

# 3. Seed the database with realistic demo data
python -m app.seed

# 4. Run the CLI
python main.py

# 5. (Optional) Run the unit tests
python -m pytest tests/ -v
```

## Tech Stack

- **Python 3** — application logic
- **SQLite** — relational data storage (zero-setup, file-based)
- **pytest** — unit testing

## Possible Extensions

- REST API layer (Flask/FastAPI) exposing the same `ticket_service` functions
- SLA timers based on priority (e.g. Critical must be resolved within 4 hours)
- Web dashboard for ticket queues and reporting
- Role-based access (end user vs. technician vs. admin)

## Author

Built as a portfolio project to demonstrate ITSM concepts (incident and
service request management, impact/urgency prioritization, troubleshooting
documentation, and escalation workflows) alongside practical Python and SQL
skills.
