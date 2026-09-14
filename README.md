# 🛒 E-Commerce Backend Service & Integration Test Suite

A containerized e-commerce backend built with **Java 21** and **Spring Boot 3.3.5**, featuring clean domain-driven architecture for **Product** and **Order** management, robust validation, inventory tracking, and an extensive **JUnit 5** integration test suite with both happy and negative test paths.

---

## 📋 Features

- **Product Service**: Create and retrieve products, track real-time stock levels, and safely handle inventory deductions and cancellations.
- **Order Service**: Place orders against available product inventory, automatically calculate totals, and update order status/shipping address.
- **Inventory Consistency**: Atomic inventory decrement upon placing orders and automated inventory restoration if an order is cancelled.
- **Terminal State Protection**: Negative business constraints preventing modification of orders that have already reached terminal states (`CANCELLED` or `SHIPPED`).
- **Structured Error Handling**: Centralized `@RestControllerAdvice` emitting standardized JSON responses for validation errors (400), business constraint violations (400), and missing resources (404).
- **Integration Test Suite**: 8 end-to-end tests verifying HTTP contracts and database states using JUnit 5 and `MockMvc`.
- **Dockerized Multi-Stage Build**: Production-ready, non-root Alpine container with healthchecks and JVM container optimization.

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| **Language** | Java 21 LTS |
| **Framework** | Spring Boot 3.3.5 |
| **Persistence** | Spring Data JPA & Hibernate 6.5 |
| **Database** | H2 In-Memory Database |
| **Validation** | Jakarta Bean Validation |
| **Testing** | JUnit 5, MockMvc, AssertJ, Spring Test |
| **Containerization** | Docker (Multi-stage build), Docker Compose |

---

## 🚀 Quick Start with Docker

### Option 1: Docker Compose (Recommended)

Run the entire application with a single command:

```bash
docker compose up --build
```

To run in the background (detached mode):
```bash
docker compose up --build -d
```

To stop:
```bash
docker compose down
```

### Option 2: Standalone Docker

1. **Build the image**:
   ```bash
   docker build -t ecommerce-service:latest .
   ```

2. **Run the container**:
   ```bash
   docker run -d -p 8080:8080 --name ecommerce-backend ecommerce-service:latest
   ```

3. **Check container logs**:
   ```bash
   docker logs -f ecommerce-backend
   ```

4. **Stop the container**:
   ```bash
   docker stop ecommerce-backend && docker rm ecommerce-backend
   ```

The application will be accessible at: `http://localhost:8080`

---

## 💻 Running Locally without Docker

### Prerequisites
- Java 21 JDK
- Maven 3.9+ (or use the included `./mvnw` wrapper)

### Build & Run
```bash
# Using Maven wrapper (Linux/macOS)
./mvnw spring-boot:run

# Using Maven wrapper (Windows PowerShell)
.\mvnw.cmd spring-boot:run

# Or using installed Maven
mvn spring-boot:run
```

---

## 🧪 Running Integration Tests

Execute the full integration test suite (8 tests covering both happy and negative paths):

```bash
mvn clean test
```

### Test Suite Breakdown

| # | Test Case | Scenario | Path | Description |
|---|---|---|---|---|
| 1 | `createProduct_ValidPayload_Returns201AndPersistsInDb` | Create Product | Happy | Asserts HTTP 201 and verifies DB persistence. |
| 2 | `createProduct_InvalidPayload_BlankName_Returns400` | Create Product | Negative | Rejects blank product name with HTTP 400. |
| 3 | `placeOrder_ValidProductAndStock_Returns201AndDeductsInventory` | Place Order | Happy | Asserts HTTP 201 and verifies product stock was deducted. |
| 4 | `placeOrder_InsufficientStock_Returns400AndDoesNotCreateOrder` | Place Order | Negative | Rejects order exceeding available inventory with HTTP 400. |
| 5 | `updateOrder_ValidAddressAndStatus_Returns200AndUpdatesState` | Update Order | Happy | Updates shipping address and transitions status to `SHIPPED`. |
| 6 | `updateOrder_NonExistentOrder_Returns404` | Update Order | Negative | Rejects updating an unknown order ID with HTTP 404. |
| 7 | `updateOrder_AlreadyCancelled_Returns400` | Update Order | Negative | Rejects modifying an order already in `CANCELLED` status. |
| 8 | `updateOrder_CancelOrder_RestoresProductStock` | Update Order | State Transition | Cancelling an order automatically returns stock to the product. |

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

**Response (`201 Created`):**
```json
{
  "id": 1,
  "name": "Wireless Noise Cancelling Headphones",
  "description": "High-fidelity Bluetooth over-ear headphones",
  "price": 199.99,
  "stock": 50
}
```

---

### 2. Retrieve All Products
```bash
curl -X GET http://localhost:8080/api/products
```

---

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

**Response (`201 Created`):**
```json
{
  "id": 1,
  "productId": 1,
  "quantity": 2,
  "totalAmount": 399.98,
  "shippingAddress": "742 Evergreen Terrace, Springfield",
  "status": "CONFIRMED",
  "createdAt": "2026-09-14T04:20:00Z"
}
```

---

### 4. Update an Order
```bash
curl -X PUT http://localhost:8080/api/orders/1 \
  -H "Content-Type: application/json" \
  -d '{
    "shippingAddress": "100 Industrial Parkway, Suite 300",
    "status": "SHIPPED"
  }'
```

---

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
├── Dockerfile                  # Multi-stage production container build
├── docker-compose.yml          # Container orchestration configuration
├── pom.xml                     # Maven dependencies & build setup
├── README.md                   # Project documentation
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
    │       └── application.yml
    └── test/
        ├── java/com/ecommerce/
        │   └── ECommerceIntegrationTest.java
        └── resources/
            └── application-test.yml
```
