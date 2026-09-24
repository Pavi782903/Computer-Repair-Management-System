CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    address VARCHAR(200) NOT NULL
);

CREATE TABLE devices (
    device_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    device_type VARCHAR(50) NOT NULL,
    brand VARCHAR(50) NOT NULL,
    model VARCHAR(100) NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE repairs (
    repair_id INTEGER PRIMARY KEY,
    device_id INTEGER NOT NULL,
    problem TEXT NOT NULL,
    repair_cost FLOAT NOT NULL CHECK (repair_cost >= 0),
    repair_status VARCHAR(20) NOT NULL CHECK (repair_status IN ('Pending', 'In Progress', 'Completed', 'Delivered')),
    FOREIGN KEY (device_id) REFERENCES devices(device_id)
);

INSERT INTO customers (customer_id, customer_name, phone_number, address) VALUES
(1, 'Rahul', '9876543210', 'Hyderabad'),
(2, 'Arjun', '9876543211', 'Chennai'),
(3, 'Priya', '9876543212', 'Bangalore');

INSERT INTO devices (device_id, customer_id, device_type, brand, model) VALUES
(1, 1, 'Laptop', 'Dell', 'Inspiron 15'),
(2, 2, 'Desktop', 'HP', 'Pavilion'),
(3, 3, 'Laptop', 'Lenovo', 'IdeaPad 3');

INSERT INTO repairs (repair_id, device_id, problem, repair_cost, repair_status) VALUES
(1, 1, 'Laptop not powering on', 1500, 'Pending'),
(2, 2, 'System overheating', 2000, 'In Progress'),
(3, 3, 'Screen problem', 3500, 'Completed');
