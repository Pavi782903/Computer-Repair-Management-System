from sqlalchemy import Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Customer(Base):
    __tablename__ = "customers"

    customer_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    customer_name: Mapped[str] = mapped_column(String(100), nullable=False)
    phone_number: Mapped[str] = mapped_column(String(20), nullable=False)
    address: Mapped[str] = mapped_column(String(200), nullable=False)

    devices: Mapped[list["Device"]] = relationship(
        back_populates="customer", cascade="all, delete-orphan"
    )


class Device(Base):
    __tablename__ = "devices"

    device_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.customer_id"), nullable=False, index=True)
    device_type: Mapped[str] = mapped_column(String(50), nullable=False)
    brand: Mapped[str] = mapped_column(String(50), nullable=False)
    model: Mapped[str] = mapped_column(String(100), nullable=False)

    customer: Mapped[Customer] = relationship(back_populates="devices")
    repairs: Mapped[list["Repair"]] = relationship(
        back_populates="device", cascade="all, delete-orphan"
    )


class Repair(Base):
    __tablename__ = "repairs"

    repair_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    device_id: Mapped[int] = mapped_column(ForeignKey("devices.device_id"), nullable=False, index=True)
    problem: Mapped[str] = mapped_column(Text, nullable=False)
    repair_cost: Mapped[float] = mapped_column(Float, nullable=False)
    repair_status: Mapped[str] = mapped_column(String(20), nullable=False)

    device: Mapped[Device] = relationship(back_populates="repairs")
