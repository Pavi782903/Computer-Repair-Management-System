from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class RepairStatus(str, Enum):
    pending = "Pending"
    in_progress = "In Progress"
    completed = "Completed"
    delivered = "Delivered"


class CustomerBase(BaseModel):
    customer_name: str = Field(min_length=1, max_length=100)
    phone_number: str = Field(min_length=1, max_length=20)
    address: str = Field(min_length=1, max_length=200)


class CustomerCreate(CustomerBase):
    pass


class CustomerResponse(CustomerBase):
    model_config = ConfigDict(from_attributes=True)

    customer_id: int


class DeviceBase(BaseModel):
    device_type: str = Field(min_length=1, max_length=50)
    brand: str = Field(min_length=1, max_length=50)
    model: str = Field(min_length=1, max_length=100)


class DeviceCreate(DeviceBase):
    customer_id: int = Field(gt=0)


class DeviceResponse(DeviceBase):
    model_config = ConfigDict(from_attributes=True)

    device_id: int
    customer_id: int


class RepairBase(BaseModel):
    problem: str = Field(min_length=1)
    repair_cost: float = Field(ge=0)


class RepairCreate(RepairBase):
    device_id: int = Field(gt=0)
    repair_status: RepairStatus = RepairStatus.pending


class RepairStatusUpdate(BaseModel):
    repair_status: RepairStatus


class RepairResponse(RepairBase):
    model_config = ConfigDict(from_attributes=True)

    repair_id: int
    device_id: int
    repair_status: RepairStatus
