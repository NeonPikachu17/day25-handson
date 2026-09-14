# 🧪 Integration Testing Documentation

Comprehensive documentation for the integration testing suite implemented for **Task 1: Integration Testing** of the E-Commerce backend service.

---

## 📌 Executive Summary

| Item | Details |
|---|---|
| **Task** | Task 1: Integration Testing |
| **Required Scenarios** | 1. Create a new product<br>2. Place a new order<br>3. Update an existing order |
| **Minimum Required Cases** | At least 5 test cases |
| **Implemented Test Cases** | **15 test cases** (300% of requirement) |
| **Test Framework** | JUnit 5 (Jupiter), Spring Test (`MockMvc`), AssertJ |
| **Target Test Class** | [`ECommerceIntegrationTest.java`](file:///c:/Users/ABS83779/.gemini/antigravity-ide/scratch/day-25/day25-handson/src/test/java/com/ecommerce/ECommerceIntegrationTest.java) |
| **Execution Status** | **15 Passed, 0 Failures, 0 Errors, 0 Skipped** (`BUILD SUCCESS`) |

---

## 🏗️ Architecture & Test Setup

The integration test suite runs full-stack slice tests using Spring Boot's testing infrastructure, validating requests from the HTTP controller layer through services down to the relational database persistence layer.

### Key Annotations & Tools

| Annotation / Tool | Purpose |
|---|---|
| `@SpringBootTest` | Boots the full Spring ApplicationContext with real beans and domain services. |
| `@AutoConfigureMockMvc` | Automatically provides and configures `MockMvc` to perform mock HTTP requests without starting a network server. |
| `@ActiveProfiles("test")` | Activates `application-test.yml`, using an isolated, in-memory H2 database (`jdbc:h2:mem:testdb`). |
| `@Nested` | Groups test cases hierarchically by scenario for clean reporting and IDE organization. |
| `@DisplayName` | Provides human-readable descriptions of what each test proves. |
| `@BeforeEach` | Purges both `orders` and `products` tables between tests ensuring clean isolation and zero test coupling. |
| `AssertJ` & `MockMvcResultMatchers` | Fluent assertions for HTTP status codes, JSON response body paths, and database entity state. |

---

## 📊 Test Case Coverage Matrix

The suite covers **Happy Paths**, **Negative Paths (Validation & Error Handling)**, **State Machine Constraints**, and **Data Consistency**:

```
                              Integration Test Suite (15 Tests)
                                              │
         ┌────────────────────────────────────┼────────────────────────────────────┐
         ▼                                    ▼                                    ▼
Scenario 1: Create Product           Scenario 2: Place Order             Scenario 3: Update Order
  ├─ 1. Happy (201 + DB verify)        ├─ 5. Happy (201 + stock deduct)    ├─ 10. Happy (200 + address & status)
  ├─ 2. Blank Name (400)               ├─ 6. Insufficient Stock (400)      ├─ 11. Address Only (200 + status kept)
  ├─ 3. Negative Price/Stock (400)     ├─ 7. Product Not Found (404)       ├─ 12. Non-existent Order (404)
  └─ 4. Read-after-create (200)        ├─ 8. Quantity Zero (400)           ├─ 13. Terminal CANCELLED (400)
                                       └─ 9. Blank Address (400)           ├─ 14. Terminal SHIPPED (400)
                                                                           └─ 15. Stock Restored on Cancel (200)
```

---

## 🔬 Detailed Test Catalog

### Scenario 1: Create a New Product

#### Test 1: `createProduct_ValidPayload_Returns201AndPersistsInDb`
* **Type**: Happy Path
* **Method**: `POST /api/products`
* **Request Body**:
  ```json
  {
    "name": "Noise Cancelling Headphones",
    "description": "Premium wireless over-ear headphones",
    "price": 199.99,
    "stock": 50
  }
  ```
* **Verifications**:
  1. HTTP Status `201 Created`
  2. JSON Response contains non-null `id`, correct `name`, `price`, and `stock`.
  3. Direct database lookup via `productRepository.findById(createdId)` confirms entity was persisted with exact fields.

#### Test 2: `createProduct_InvalidPayload_BlankName_Returns400`
* **Type**: Negative Path (Bean Validation)
* **Method**: `POST /api/products`
* **Request Body**: Name set to empty string `""`
* **Verifications**:
  1. HTTP Status `400 Bad Request`
  2. JSON error response has `status: 400`, `error: "Validation Failed"`, and field error `errors.name`.
  3. Database count remains `0`.

#### Test 3: `createProduct_InvalidPayload_NegativePriceAndStock_Returns400`
* **Type**: Negative Path (Boundary / Bean Validation)
* **Method**: `POST /api/products`
* **Request Body**: `price: -25.50`, `stock: -10`
* **Verifications**:
  1. HTTP Status `400 Bad Request`
  2. Validation errors emitted for both `errors.price` (`@Positive`) and `errors.stock` (`@PositiveOrZero`).
  3. No record created in database.

#### Test 4: `createProduct_ThenGetById_Returns200WithAccurateDetails`
* **Type**: Happy Path (Read-After-Create Flow)
* **Method**: `POST /api/products` followed by `GET /api/products/{id}`
* **Verifications**:
  1. Create returns `201 Created`.
  2. Subsequent GET with the created ID returns `200 OK`.
  3. Validates end-to-end data read consistency across endpoints.

---

### Scenario 2: Place a New Order

#### Test 5: `placeOrder_ValidProductAndStock_Returns201AndDeductsInventory`
* **Type**: Happy Path & Business Logic
* **Setup**: Pre-save Product in DB with `price: 89.50`, `stock: 10`.
* **Method**: `POST /api/orders`
* **Request Body**:
  ```json
  {
    "productId": 1,
    "quantity": 3,
    "shippingAddress": "123 Tech Lane, Silicon Valley, CA"
  }
  ```
* **Verifications**:
  1. HTTP Status `201 Created`.
  2. Total amount calculated accurately: `89.50 * 3 = 268.50`.
  3. Order saved in DB with status `CONFIRMED`.
  4. **Inventory side-effect**: Product stock decremented from `10` to `7` (`10 - 3 = 7`).

#### Test 6: `placeOrder_InsufficientStock_Returns400AndDoesNotCreateOrder`
* **Type**: Negative Path (Business Constraint)
* **Setup**: Product has `stock: 2`.
* **Method**: `POST /api/orders` requesting `quantity: 5`.
* **Verifications**:
  1. HTTP Status `400 Bad Request`.
  2. JSON response: `error: "Insufficient Stock"`.
  3. Zero orders created in DB (`orderRepository.count() == 0`).
  4. Product stock untouched (`stock == 2`).

#### Test 7: `placeOrder_NonExistentProduct_Returns404`
* **Type**: Negative Path (Resource Missing)
* **Method**: `POST /api/orders` with `productId: 999999`.
* **Verifications**:
  1. HTTP Status `404 Not Found`.
  2. Error message explicitly informs: `"Product not found with id: 999999"`.
  3. No order persisted.

#### Test 8: `placeOrder_InvalidQuantityZero_Returns400`
* **Type**: Negative Path (Bean Validation)
* **Method**: `POST /api/orders` with `quantity: 0`.
* **Verifications**:
  1. HTTP Status `400 Bad Request`.
  2. Error payload flags `errors.quantity` violation (`@Min(1)`).

#### Test 9: `placeOrder_BlankShippingAddress_Returns400`
* **Type**: Negative Path (Bean Validation)
* **Method**: `POST /api/orders` with `shippingAddress: "   "`.
* **Verifications**:
  1. HTTP Status `400 Bad Request`.
  2. Field error triggered for `errors.shippingAddress` (`@NotBlank`).

---

### Scenario 3: Update an Existing Order

#### Test 10: `updateOrder_ValidAddressAndStatus_Returns200AndUpdatesState`
* **Type**: Happy Path (Full Update)
* **Setup**: Order exists in `CONFIRMED` status.
* **Method**: `PUT /api/orders/{id}`
* **Request Body**:
  ```json
  {
    "shippingAddress": "New Address 200, Suite 5B",
    "status": "SHIPPED"
  }
  ```
* **Verifications**:
  1. HTTP Status `200 OK`.
  2. Shipping address updated to `"New Address 200, Suite 5B"`.
  3. Status updated to `"SHIPPED"`.
  4. Verified directly in DB.

#### Test 11: `updateOrder_AddressOnly_Returns200AndPreservesStatus`
* **Type**: Happy Path (Partial Update)
* **Method**: `PUT /api/orders/{id}` with `shippingAddress` updated and `status: null`.
* **Verifications**:
  1. HTTP Status `200 OK`.
  2. Address is changed.
  3. Status remains preserved as `CONFIRMED`.

#### Test 12: `updateOrder_NonExistentOrder_Returns404`
* **Type**: Negative Path (Resource Missing)
* **Method**: `PUT /api/orders/999999`
* **Verifications**:
  1. HTTP Status `404 Not Found`.
  2. JSON body `status: 404`, `error: "Not Found"`.

#### Test 13: `updateOrder_AlreadyCancelled_Returns400`
* **Type**: Negative Path (Terminal State Protection)
* **Setup**: Order is in `CANCELLED` status.
* **Method**: `PUT /api/orders/{id}`
* **Verifications**:
  1. HTTP Status `400 Bad Request`.
  2. Message indicates `"Cannot update order in CANCELLED status"`.

#### Test 14: `updateOrder_AlreadyShipped_Returns400`
* **Type**: Negative Path (Terminal State Protection)
* **Setup**: Order is in `SHIPPED` status.
* **Method**: `PUT /api/orders/{id}`
* **Verifications**:
  1. HTTP Status `400 Bad Request`.
  2. Message indicates `"Cannot update order in SHIPPED status"`.

#### Test 15: `updateOrder_CancelOrder_RestoresProductStock`
* **Type**: State Transition & Inventory Integrity
* **Setup**: Product started with 10 units, 3 units ordered → current stock is `7`. Order status is `CONFIRMED`.
* **Method**: `PUT /api/orders/{id}` with `status: "CANCELLED"`.
* **Verifications**:
  1. HTTP Status `200 OK`.
  2. Order status transitions to `"CANCELLED"`.
  3. **Automatic stock restoration**: Product inventory reloaded from database proves that stock increased from `7` back to `10` (`7 + 3 = 10`).

---

## 🚀 How to Execute the Tests

### 1. Execute All Integration Tests
In terminal / PowerShell at project root:
```powershell
# Windows
.\mvnw.cmd test -Dtest=ECommerceIntegrationTest

# Linux / macOS
./mvnw test -Dtest=ECommerceIntegrationTest
```

### 2. Execute a Single Scenario Group (Nested Class)
```powershell
# Run only Create Product scenario tests
.\mvnw.cmd test -Dtest=ECommerceIntegrationTest$CreateProductTests

# Run only Place Order scenario tests
.\mvnw.cmd test -Dtest=ECommerceIntegrationTest$PlaceOrderTests

# Run only Update Order scenario tests
.\mvnw.cmd test -Dtest=ECommerceIntegrationTest$UpdateOrderTests
```

### 3. Execute an Individual Test Method
```powershell
.\mvnw.cmd test -Dtest=ECommerceIntegrationTest$UpdateOrderTests#updateOrder_CancelOrder_RestoresProductStock
```

### 4. Execute the Entire Test Suite
```powershell
.\mvnw.cmd clean test
```

---

## 📈 Test Results & Verification Log

```
-------------------------------------------------------
 T E S T S
-------------------------------------------------------
Running com.ecommerce.ECommerceIntegrationTest
2026-09-14T14:10:33.151+08:00  INFO 14324 --- [ecommerce-service] [main] com.ecommerce.ECommerceIntegrationTest : Starting ECommerceIntegrationTest using Java 21.0.8
2026-09-14T14:10:33.152+08:00  INFO 14324 --- [ecommerce-service] [main] com.ecommerce.ECommerceIntegrationTest : The following 1 profile is active: "test"
...
[INFO] Tests run: 15, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 6.945 s -- in com.ecommerce.ECommerceIntegrationTest
[INFO] 
[INFO] Results:
[INFO] 
[INFO] Tests run: 15, Failures: 0, Errors: 0, Skipped: 0
[INFO] 
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
[INFO] Total time: 11.758 s
```

---

## 💡 Best Practices Implemented

1. **Deterministic Isolation**: `deleteAll()` inside `@BeforeEach` ensures no lingering state spills across tests.
2. **Layered Verification**: Tests don't just inspect the HTTP JSON response; they cross-check the persistent database state via repository queries.
3. **Domain Invariant Testing**: Inventory math (deduction on order, restoration on cancellation) and business rules (terminal state immutability) are thoroughly tested.
4. **Hierarchical Organization**: Using JUnit 5 `@Nested` classes groups related tests logically under their respective scenario requirement.
