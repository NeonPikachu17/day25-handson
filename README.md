# 🛒 E-Commerce Backend Service & Integration Test Suite

A clean, production-grade e-commerce backend built with **Java 21** and **Spring Boot 3.3.5**, featuring domain-driven architecture for **Product** and **Order** management, robust validation, inventory tracking, and a **JUnit 5** integration test suite with containerized **Test Data Management** using Docker.

---

## 📋 Features

- **Product Service**: Create and retrieve products, track real-time stock levels, and handle inventory deductions/restorations.
- **Order Service**: Place orders against available product inventory, automatically calculate totals, and update order status/shipping address.
- **Inventory Consistency**: Atomic inventory decrement upon placing orders and automated inventory restoration if an order is cancelled.
- **Terminal State Protection**: Negative business constraints preventing modification of orders that have already reached terminal states (`CANCELLED` or `SHIPPED`).
- **Structured Error Handling**: Centralized `@RestControllerAdvice` emitting standardized JSON responses for validation errors (400), business constraint violations (400), and missing resources (404).
- **Test Data Management in Docker (Task 3)**: Isolated PostgreSQL test database running in Docker with pre-seeded baseline test datasets (`docker/init-test-data.sql`) ensuring deterministic, repeatable test runs without polluting production data.
- **Zero-Dependency Quickstart**: Maven Wrapper (`./mvnw` / `mvnw.cmd`) included so anyone can build and run immediately.

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| **Language** | Java 21 LTS |
| **Framework** | Spring Boot 3.3.5 |
| **Persistence** | Spring Data JPA & Hibernate 6.5 |
| **Databases** | H2 In-Memory & PostgreSQL 16 (in Docker) |
| **Validation** | Jakarta Bean Validation |
| **Testing** | JUnit 5, MockMvc, AssertJ, Spring Test |
| **Test Data Management** | Docker & Docker Compose (`postgres:16-alpine`) |

---

## 🐳 Task 3: Test Data Management with Docker

The application itself runs natively on Java, while the **test data environment is managed in Docker** to provide clean, isolated, reproducible test datasets.

### 1. Start the Docker Test Database
Launch the isolated PostgreSQL test database with pre-seeded test data:

```bash
docker compose up -d
```

This starts `ecommerce-test-db` on port `5433` and executes [`docker/init-test-data.sql`](file:///docker/init-test-data.sql), creating:
- Predictable baseline test products (e.g., `Test Gaming Laptop`, `Test Wireless Mouse`, `Test Low Stock Gadget`).
- Pre-seeded test orders for state mutation and boundary testing.

### 2. Reset / Wipe Test Data
To reset test data back to a clean state:
```bash
docker compose down -v && docker compose up -d
```

### 3. Stop the Test Database
```bash
docker compose down
```

---

## 💻 Running the Application Locally

### Prerequisites
- Java 21 JDK
- Docker (for the test database environment)

### Run Application
```bash
# Windows
.\mvnw.cmd spring-boot:run

# Linux / macOS
./mvnw spring-boot:run

# Or with installed Maven
mvn spring-boot:run
```

The application starts on `http://localhost:8080`.

---

## 🧪 Running Integration Tests

Execute the full suite of **10 integration tests** (8 core domain tests + 2 Docker test data integration tests):

```bash
mvn clean test
```

### Test Suite Summary

| # | Test Class | Scenario | Path | Description |
|---|---|---|---|---|
| 1 | `ECommerceIntegrationTest` | Create Product | Happy | Verifies HTTP 201 and database persistence. |
| 2 | `ECommerceIntegrationTest` | Create Product | Negative | Rejects blank product name with HTTP 400. |
| 3 | `ECommerceIntegrationTest` | Place Order | Happy | Verifies HTTP 201 and inventory deduction (10 → 7). |
| 4 | `ECommerceIntegrationTest` | Place Order | Negative | Rejects order exceeding stock with HTTP 400. |
| 5 | `ECommerceIntegrationTest` | Update Order | Happy | Updates shipping address and transitions status to `SHIPPED`. |
| 6 | `ECommerceIntegrationTest` | Update Order | Negative | Rejects updating non-existent order ID with HTTP 404. |
| 7 | `ECommerceIntegrationTest` | Update Order | Negative | Rejects modifying order in terminal `CANCELLED` status. |
| 8 | `ECommerceIntegrationTest` | Update Order | State Transition | Cancelling an order automatically restores inventory. |
| 9 | `DockerTestDataIntegrationTest` | Test Data Management | Verification | Verifies pre-seeded test data exists in Docker PostgreSQL. |
| 10 | `DockerTestDataIntegrationTest` | Test Data Management | Container Integration | Executes order placement and persistence directly against Docker test DB. |

---

## 📡 API Reference & Examples

### 1. Create a Product
```bash
curl -X POST http://localhost:8080/api/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Wireless Noise Cancelling Headphones",
    "description": "High-fidelity Bluetooth over-ear headphones",
    "price": 199.99,
    "stock": 50
  }'
```

### 2. Retrieve All Products
```bash
curl -X GET http://localhost:8080/api/products
```

### 3. Place a New Order
```bash
curl -X POST http://localhost:8080/api/orders \
  -H "Content-Type: application/json" \
  -d '{
    "productId": 1,
    "quantity": 2,
    "shippingAddress": "742 Evergreen Terrace, Springfield"
  }'
```

### 4. Update an Order
```bash
curl -X PUT http://localhost:8080/api/orders/1 \
  -H "Content-Type: application/json" \
  -d '{
    "shippingAddress": "100 Industrial Parkway, Suite 300",
    "status": "SHIPPED"
  }'
```

### 5. Cancel an Order (Restores Stock)
```bash
curl -X PUT http://localhost:8080/api/orders/1 \
  -H "Content-Type: application/json" \
  -d '{
    "status": "CANCELLED"
  }'
```

---

## 📂 Project Structure

```
day-25/
├── docker/
│   └── init-test-data.sql          # Test data initialization & baseline seed script
├── docker-compose.yml              # Docker container for isolated PostgreSQL test database
├── pom.xml                         # Maven dependencies & build setup
├── README.md                       # Project documentation
└── src/
    ├── main/
    │   ├── java/com/ecommerce/
    │   │   ├── ECommerceApplication.java
    │   │   ├── exception/
    │   │   │   ├── GlobalExceptionHandler.java
    │   │   │   ├── InsufficientStockException.java
    │   │   │   └── ResourceNotFoundException.java
    │   │   ├── product/
    │   │   │   ├── Product.java
    │   │   │   ├── ProductRepository.java
    │   │   │   ├── ProductService.java
    │   │   │   ├── ProductController.java
    │   │   │   └── dto/
    │   │   │       ├── CreateProductRequest.java
    │   │   │       └── ProductResponse.java
    │   │   └── order/
    │   │       ├── Order.java
    │   │       ├── OrderStatus.java
    │   │       ├── OrderRepository.java
    │   │       ├── OrderService.java
    │   │       ├── OrderController.java
    │   │       └── dto/
    │   │           ├── PlaceOrderRequest.java
    │   │           ├── UpdateOrderRequest.java
    │   │           └── OrderResponse.java
    │   └── resources/
    │       ├── application.yml
    │       └── application-docker.yml
    └── test/
        ├── java/com/ecommerce/
        │   ├── ECommerceIntegrationTest.java
        │   └── DockerTestDataIntegrationTest.java
        └── resources/
            └── application-test.yml
```
