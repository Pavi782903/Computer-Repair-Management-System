from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import Customer, Device, Repair
from schemas import (
    CustomerCreate,
    CustomerResponse,
    DeviceCreate,
    DeviceResponse,
    RepairCreate,
    RepairResponse,
    RepairStatus,
    RepairStatusUpdate,
)


def seed_database() -> None:
    db = next(get_db())
    try:
        if db.query(Customer).count() > 0:
            return
        customers = [
            Customer(customer_id=1, customer_name="Rahul", phone_number="9876543210", address="Hyderabad"),
            Customer(customer_id=2, customer_name="Arjun", phone_number="9876543211", address="Chennai"),
            Customer(customer_id=3, customer_name="Priya", phone_number="9876543212", address="Bangalore"),
        ]
        devices = [
            Device(device_id=1, customer_id=1, device_type="Laptop", brand="Dell", model="Inspiron 15"),
            Device(device_id=2, customer_id=2, device_type="Desktop", brand="HP", model="Pavilion"),
            Device(device_id=3, customer_id=3, device_type="Laptop", brand="Lenovo", model="IdeaPad 3"),
        ]
        repairs = [
            Repair(repair_id=1, device_id=1, problem="Laptop not powering on", repair_cost=1500, repair_status="Pending"),
            Repair(repair_id=2, device_id=2, problem="System overheating", repair_cost=2000, repair_status="In Progress"),
            Repair(repair_id=3, device_id=3, problem="Screen problem", repair_cost=3500, repair_status="Completed"),
        ]
        db.add_all(customers + devices + repairs)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise
    finally:
        db.close()


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    seed_database()
    yield


app = FastAPI(
    title="Computer Repair Management System",
    description="CRUD APIs for customers, devices, and repairs.",
    version="1.0.0",
    lifespan=lifespan,
)


def get_or_404(db: Session, model: type, item_id: int, label: str):
    item = db.get(model, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail=f"{label} with ID {item_id} not found")
    return item


@app.post("/customers", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED, tags=["Customers"])
def add_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    try:
        item = Customer(**customer.model_dump())
        db.add(item)
        db.commit()
        db.refresh(item)
        return item
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Unable to add customer")


@app.get("/customers", response_model=list[CustomerResponse], tags=["Customers"])
def view_customers(name: str | None = Query(default=None), db: Session = Depends(get_db)):
    query = db.query(Customer)
    if name:
        query = query.filter(Customer.customer_name.ilike(f"%{name}%"))
    return query.order_by(Customer.customer_id).all()


@app.get("/customers/{customer_id}", response_model=CustomerResponse, tags=["Customers"])
def search_customer(customer_id: int, db: Session = Depends(get_db)):
    return get_or_404(db, Customer, customer_id, "Customer")


@app.put("/customers/{customer_id}", response_model=CustomerResponse, tags=["Customers"])
def update_customer(customer_id: int, customer: CustomerCreate, db: Session = Depends(get_db)):
    item = get_or_404(db, Customer, customer_id, "Customer")
    try:
        for key, value in customer.model_dump().items():
            setattr(item, key, value)
        db.commit()
        db.refresh(item)
        return item
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Unable to update customer")


@app.delete("/customers/{customer_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Customers"])
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    item = get_or_404(db, Customer, customer_id, "Customer")
    try:
        db.delete(item)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Unable to delete customer")


@app.post("/devices", response_model=DeviceResponse, status_code=status.HTTP_201_CREATED, tags=["Devices"])
def add_device(device: DeviceCreate, db: Session = Depends(get_db)):
    get_or_404(db, Customer, device.customer_id, "Customer")
    try:
        item = Device(**device.model_dump())
        db.add(item)
        db.commit()
        db.refresh(item)
        return item
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Unable to add device")


@app.get("/devices", response_model=list[DeviceResponse], tags=["Devices"])
def view_devices(customer_id: int | None = Query(default=None, gt=0), db: Session = Depends(get_db)):
    query = db.query(Device)
    if customer_id is not None:
        query = query.filter(Device.customer_id == customer_id)
    return query.order_by(Device.device_id).all()


@app.get("/devices/{device_id}", response_model=DeviceResponse, tags=["Devices"])
def search_device(device_id: int, db: Session = Depends(get_db)):
    return get_or_404(db, Device, device_id, "Device")


@app.put("/devices/{device_id}", response_model=DeviceResponse, tags=["Devices"])
def update_device(device_id: int, device: DeviceCreate, db: Session = Depends(get_db)):
    item = get_or_404(db, Device, device_id, "Device")
    get_or_404(db, Customer, device.customer_id, "Customer")
    try:
        for key, value in device.model_dump().items():
            setattr(item, key, value)
        db.commit()
        db.refresh(item)
        return item
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Unable to update device")


@app.delete("/devices/{device_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Devices"])
def delete_device(device_id: int, db: Session = Depends(get_db)):
    item = get_or_404(db, Device, device_id, "Device")
    try:
        db.delete(item)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Unable to delete device")


@app.post("/repairs", response_model=RepairResponse, status_code=status.HTTP_201_CREATED, tags=["Repairs"])
def create_repair(repair: RepairCreate, db: Session = Depends(get_db)):
    get_or_404(db, Device, repair.device_id, "Device")
    try:
        values = repair.model_dump()
        values["repair_status"] = values["repair_status"].value
        item = Repair(**values)
        db.add(item)
        db.commit()
        db.refresh(item)
        return item
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Unable to create repair")


@app.get("/repairs", response_model=list[RepairResponse], tags=["Repairs"])
def view_repairs(status_filter: RepairStatus | None = Query(default=None, alias="status"), db: Session = Depends(get_db)):
    query = db.query(Repair)
    if status_filter:
        query = query.filter(Repair.repair_status == status_filter.value)
    return query.order_by(Repair.repair_id).all()


@app.get("/repairs/{repair_id}", response_model=RepairResponse, tags=["Repairs"])
def search_repair(repair_id: int, db: Session = Depends(get_db)):
    return get_or_404(db, Repair, repair_id, "Repair")


@app.put("/repairs/{repair_id}/status", response_model=RepairResponse, tags=["Repairs"])
def update_repair_status(repair_id: int, update: RepairStatusUpdate, db: Session = Depends(get_db)):
    item = get_or_404(db, Repair, repair_id, "Repair")
    try:
        item.repair_status = update.repair_status.value
        db.commit()
        db.refresh(item)
        return item
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Unable to update repair status")


@app.delete("/repairs/{repair_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Repairs"])
def delete_repair(repair_id: int, db: Session = Depends(get_db)):
    item = get_or_404(db, Repair, repair_id, "Repair")
    try:
        db.delete(item)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Unable to delete repair")
