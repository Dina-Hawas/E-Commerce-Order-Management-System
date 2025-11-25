# E-Commerce Order Management System

## Course & Assignment
- *Course:* Service-Oriented Architecture  
- *Assignment Type:* Programming Project  
- *Duration:* 4-6 weeks  
- *Team Size:* 3-4 students (or individual)  
- *Total Points:* 100  

---

## Project Overview
This project demonstrates a *microservices-based E-Commerce Order Management System*.  
The system consists of:

- *Frontend:* Java JSP web application serving as API gateway and user interface  
- *Backend:* Five independent Python Flask microservices handling different business logic  
- *Database:* MySQL 8.0  

The system implements service orchestration, RESTful APIs, and database integration.

---

## Core Architecture
- Java JSP application communicates with *five Flask microservices* via HTTP REST APIs  
- Each service runs on a *separate port*  
- Two or more services interact with the *MySQL database*  
- Microservices are independent and modular

### Microservices and Ports
| Service | Port | Responsibilities |
|---------|------|-----------------|
| Order Service | 5001 | Accept orders, validate input, generate order ID, return confirmation |
| Inventory Service | 5002 | Check stock availability, update inventory, maintain product catalog |
| Pricing Service | 5003 | Calculate pricing, apply discounts, query database |
| Customer Service | 5004 | Manage customer profiles, order history, loyalty points |
| Notification Service | 5005 | Send notifications (simulate email/SMS), log notifications |

---

## Technology Stack
- *Frontend:* Java JSP with Jakarta EE (Servlets)  
- *Backend:* Python 3.8+ with Flask  
- *Database:* MySQL 8.0  
- *Web Server:* Apache Tomcat 10.x  
- *API Communication:* REST with JSON  

---

## Project Structure
C:\Ecommerce-SOA
├─ services/
│ ├─ order_service/
│ ├─ inventory_service/
│ ├─ pricing_service/
│ ├─ customer_service/
│ └─ notification_service/
└─ database/
└─ ecommerce_system.sql

yaml
نسخ الكود

---

## Database Setup
1. Create database:

```sql
CREATE DATABASE ecommerce_system;
USE ecommerce_system;
Create tables for each service (examples):

sql
نسخ الكود
-- Inventory
CREATE TABLE inventory (
    product_id INT PRIMARY KEY AUTO_INCREMENT,
    product_name VARCHAR(100) NOT NULL,
    quantity_available INT NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Customers
CREATE TABLE customers (
    customer_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    loyalty_points INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Pricing Rules
CREATE TABLE pricing_rules (
    rule_id INT PRIMARY KEY AUTO_INCREMENT,
    product_id INT,
    min_quantity INT,
    discount_percentage DECIMAL(5,2)
);

-- Notification Log
CREATE TABLE notification_log (
    notification_id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT NOT NULL,
    customer_id INT NOT NULL,
    notification_type VARCHAR(50),
    message TEXT,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
Insert sample data (products, customers, pricing rules) as provided in the assignment.

Optional: Create a database user with limited privileges:

sql
نسخ الكود
CREATE USER 'ecommerce_user'@'localhost' IDENTIFIED BY 'secure_password';
GRANT SELECT, INSERT, UPDATE ON ecommerce_system.* TO 'ecommerce_user'@'localhost';
FLUSH PRIVILEGES;
Running the Project
Backend Services (Python Flask)
Navigate to each service folder:

cmd
نسخ الكود
cd services\inventory_service
Activate the virtual environment:

cmd
نسخ الكود
inventory_env\Scripts\activate
Install dependencies:

cmd
نسخ الكود
pip install flask mysql-connector-python requests
Run the service:

cmd
نسخ الكود
python app.py
Repeat for each microservice on its respective port.

Frontend (Java JSP)
Open the project in NetBeans or any Jakarta EE compatible IDE.

Add Jakarta EE API library.

Run the project on Apache Tomcat.

Access pages:

index.jsp → Product catalog

checkout.jsp → Place an order

confirmation.jsp → Order success page

Inter-Service Communication
Java JSP application sends requests to Flask services via HTTP REST

Flask services may call each other using Python requests library

Example:

python
نسخ الكود
import requests
response = requests.get(f"http://localhost:5002/api/inventory/check/{product_id}")
product_data = response.json()
Team Collaboration
Use GitHub for version control

Ignore virtual environments and compiled files via .gitignore:

bash
نسخ الكود
services/*/inventory_env/
services/*/_pycache_/
*.pyc
Each team member should clone the repo and activate virtual environments before running services.

Notes
Ensure MySQL server is running and accessible by services

Ports must be consistent to avoid conflicts

Use db_config_template.py to create service-specific db_config.py with credentials
