# Computer Repair Management System

A clean FastAPI + SQLAlchemy REST API for managing customers, devices, and repairs in a SQLite SQL database.

## Features

- Customer, device, and repair CRUD APIs
- SQLAlchemy ORM relationships with foreign keys
- Pydantic request and response validation
- Seeded with the three requested customers, devices, and repairs
- Customer and device foreign-key validation
- Non-negative repair cost validation
- Controlled repair statuses: `Pending`, `In Progress`, `Completed`, `Delivered`
- Interactive Swagger UI at `/docs`
- ReDoc documentation at `/redoc`

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload
```

Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to test every endpoint in Swagger UI.

The SQLite database file `repair_management.db` is created automatically on first startup. The application inserts the example records only when the customers table is empty.

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/customers` | Add customer |
| GET | `/customers` | View all customers; optional `name` search |
| GET | `/customers/{customer_id}` | Search customer by ID |
| PUT | `/customers/{customer_id}` | Update customer |
| DELETE | `/customers/{customer_id}` | Delete customer and related records |
| POST | `/devices` | Add device |
| GET | `/devices` | View all devices; optional `customer_id` filter |
| GET | `/devices/{device_id}` | Search device by ID |
| PUT | `/devices/{device_id}` | Update device |
| DELETE | `/devices/{device_id}` | Delete device and related repairs |
| POST | `/repairs` | Create repair |
| GET | `/repairs` | View all repairs; optional `status` filter |
| GET | `/repairs/{repair_id}` | Search repair by ID |
| PUT | `/repairs/{repair_id}/status` | Update repair status |
| DELETE | `/repairs/{repair_id}` | Delete repair |

## SQL Script

`schema.sql` contains the equivalent table definitions and three insert statements per table for use in a SQL database client.

## Example request bodies

Create a device:

```json
{
  "customer_id": 1,
  "device_type": "Laptop",
  "brand": "Dell",
  "model": "Latitude 5440"
}
```

Create a repair:

```json
{
  "device_id": 1,
  "problem": "Battery replacement",
  "repair_cost": 1200,
  "repair_status": "Pending"
}
```

Update a repair status:

```json
{
  "repair_status": "In Progress"
}
```
