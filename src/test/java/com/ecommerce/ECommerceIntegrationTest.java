package com.ecommerce;

import com.ecommerce.order.Order;
import com.ecommerce.order.OrderRepository;
import com.ecommerce.order.OrderStatus;
import com.ecommerce.order.dto.PlaceOrderRequest;
import com.ecommerce.order.dto.UpdateOrderRequest;
import com.ecommerce.product.Product;
import com.ecommerce.product.ProductRepository;
import com.ecommerce.product.dto.CreateProductRequest;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.MvcResult;

import java.math.BigDecimal;

import static org.assertj.core.api.Assertions.assertThat;
import static org.hamcrest.Matchers.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@SpringBootTest
@AutoConfigureMockMvc
@ActiveProfiles("test")
class ECommerceIntegrationTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @Autowired
    private ProductRepository productRepository;

    @Autowired
    private OrderRepository orderRepository;

    @BeforeEach
    void setUp() {
        orderRepository.deleteAll();
        productRepository.deleteAll();
    }

    // =========================================================================
    // Scenario 1: Create a new product
    // =========================================================================
    @Nested
    @DisplayName("Scenario 1: Create a New Product")
    class CreateProductTests {

        @Test
        @DisplayName("1. Happy Path: Successfully create product, return 201 and persist in DB")
        void createProduct_ValidPayload_Returns201AndPersistsInDb() throws Exception {
            CreateProductRequest request = new CreateProductRequest(
                    "Noise Cancelling Headphones",
                    "Premium wireless over-ear headphones",
                    new BigDecimal("199.99"),
                    50
            );

            MvcResult result = mockMvc.perform(post("/api/products")
                            .contentType(MediaType.APPLICATION_JSON)
                            .content(objectMapper.writeValueAsString(request)))
                    .andExpect(status().isCreated())
                    .andExpect(jsonPath("$.id", notNullValue()))
                    .andExpect(jsonPath("$.name", is("Noise Cancelling Headphones")))
                    .andExpect(jsonPath("$.description", is("Premium wireless over-ear headphones")))
                    .andExpect(jsonPath("$.price", is(199.99)))
                    .andExpect(jsonPath("$.stock", is(50)))
                    .andReturn();

            // Verify DB persistence
            String responseString = result.getResponse().getContentAsString();
            Long createdId = objectMapper.readTree(responseString).get("id").asLong();

            Product savedProduct = productRepository.findById(createdId).orElse(null);
            assertThat(savedProduct).isNotNull();
            assertThat(savedProduct.getName()).isEqualTo("Noise Cancelling Headphones");
            assertThat(savedProduct.getPrice()).isEqualByComparingTo("199.99");
            assertThat(savedProduct.getStock()).isEqualTo(50);
        }

        @Test
        @DisplayName("2. Negative Path: Create product with blank name returns 400 Bad Request")
        void createProduct_InvalidPayload_BlankName_Returns400() throws Exception {
            CreateProductRequest request = new CreateProductRequest(
                    "",
                    "Invalid product without name",
                    new BigDecimal("49.99"),
                    10
            );

            mockMvc.perform(post("/api/products")
                            .contentType(MediaType.APPLICATION_JSON)
                            .content(objectMapper.writeValueAsString(request)))
                    .andExpect(status().isBadRequest())
                    .andExpect(jsonPath("$.status", is(400)))
                    .andExpect(jsonPath("$.error", is("Validation Failed")))
                    .andExpect(jsonPath("$.errors.name", notNullValue()));

            assertThat(productRepository.count()).isEqualTo(0);
        }

        @Test
        @DisplayName("3. Negative Path: Create product with negative price and negative stock returns 400 Bad Request")
        void createProduct_InvalidPayload_NegativePriceAndStock_Returns400() throws Exception {
            CreateProductRequest request = new CreateProductRequest(
                    "Faulty Gadget",
                    "Invalid price and stock values",
                    new BigDecimal("-25.50"),
                    -10
            );

            mockMvc.perform(post("/api/products")
                            .contentType(MediaType.APPLICATION_JSON)
                            .content(objectMapper.writeValueAsString(request)))
                    .andExpect(status().isBadRequest())
                    .andExpect(jsonPath("$.status", is(400)))
                    .andExpect(jsonPath("$.error", is("Validation Failed")))
                    .andExpect(jsonPath("$.errors.price", notNullValue()))
                    .andExpect(jsonPath("$.errors.stock", notNullValue()));

            assertThat(productRepository.count()).isEqualTo(0);
        }

        @Test
        @DisplayName("4. Read-After-Create: Create product and immediately retrieve via GET /api/products/{id}")
        void createProduct_ThenGetById_Returns200WithAccurateDetails() throws Exception {
            CreateProductRequest request = new CreateProductRequest(
                    "Mechanical Keyboard",
                    "Tactile switches with RGB",
                    new BigDecimal("129.99"),
                    30
            );

            MvcResult postResult = mockMvc.perform(post("/api/products")
                            .contentType(MediaType.APPLICATION_JSON)
                            .content(objectMapper.writeValueAsString(request)))
                    .andExpect(status().isCreated())
                    .andReturn();

            Long createdId = objectMapper.readTree(postResult.getResponse().getContentAsString()).get("id").asLong();

            mockMvc.perform(get("/api/products/" + createdId))
                    .andExpect(status().isOk())
                    .andExpect(jsonPath("$.id", is(createdId.intValue())))
                    .andExpect(jsonPath("$.name", is("Mechanical Keyboard")))
                    .andExpect(jsonPath("$.price", is(129.99)))
                    .andExpect(jsonPath("$.stock", is(30)));
        }
    }

    // =========================================================================
    // Scenario 2: Place a new order
    // =========================================================================
    @Nested
    @DisplayName("Scenario 2: Place a New Order")
    class PlaceOrderTests {

        @Test
        @DisplayName("5. Happy Path: Place order with sufficient stock returns 201 and deducts inventory")
        void placeOrder_ValidProductAndStock_Returns201AndDeductsInventory() throws Exception {
            Product product = productRepository.save(new Product(
                    "Mechanical Keyboard",
                    "RGB tactile keyboard",
                    new BigDecimal("89.50"),
                    10
            ));

            PlaceOrderRequest orderRequest = new PlaceOrderRequest(
                    product.getId(),
                    3,
                    "123 Tech Lane, Silicon Valley, CA"
            );

            MvcResult result = mockMvc.perform(post("/api/orders")
                            .contentType(MediaType.APPLICATION_JSON)
                            .content(objectMapper.writeValueAsString(orderRequest)))
                    .andExpect(status().isCreated())
                    .andExpect(jsonPath("$.id", notNullValue()))
                    .andExpect(jsonPath("$.productId", is(product.getId().intValue())))
                    .andExpect(jsonPath("$.quantity", is(3)))
                    .andExpect(jsonPath("$.totalAmount", is(268.50))) // 89.50 * 3
                    .andExpect(jsonPath("$.status", is("CONFIRMED")))
                    .andExpect(jsonPath("$.shippingAddress", is("123 Tech Lane, Silicon Valley, CA")))
                    .andReturn();

            // Assert Order saved in DB
            Long orderId = objectMapper.readTree(result.getResponse().getContentAsString()).get("id").asLong();
            Order savedOrder = orderRepository.findById(orderId).orElse(null);
            assertThat(savedOrder).isNotNull();
            assertThat(savedOrder.getStatus()).isEqualTo(OrderStatus.CONFIRMED);

            // Assert Product stock decremented: 10 - 3 = 7
            Product reloadedProduct = productRepository.findById(product.getId()).orElseThrow();
            assertThat(reloadedProduct.getStock()).isEqualTo(7);
        }

        @Test
        @DisplayName("6. Negative Path: Place order exceeding available stock returns 400 Insufficient Stock")
        void placeOrder_InsufficientStock_Returns400AndDoesNotCreateOrder() throws Exception {
            Product product = productRepository.save(new Product(
                    "Limited Edition Sneakers",
                    "Rare collector item",
                    new BigDecimal("300.00"),
                    2
            ));

            PlaceOrderRequest orderRequest = new PlaceOrderRequest(
                    product.getId(),
                    5, // Exceeds available stock (2)
                    "456 Sneaker Street, New York, NY"
            );

            mockMvc.perform(post("/api/orders")
                            .contentType(MediaType.APPLICATION_JSON)
                            .content(objectMapper.writeValueAsString(orderRequest)))
                    .andExpect(status().isBadRequest())
                    .andExpect(jsonPath("$.status", is(400)))
                    .andExpect(jsonPath("$.error", is("Insufficient Stock")));

            // Verify no order was saved
            assertThat(orderRepository.count()).isEqualTo(0);

            // Verify product stock remained untouched
            Product reloadedProduct = productRepository.findById(product.getId()).orElseThrow();
            assertThat(reloadedProduct.getStock()).isEqualTo(2);
        }

        @Test
        @DisplayName("7. Negative Path: Place order for non-existent product ID returns 404 Not Found")
        void placeOrder_NonExistentProduct_Returns404() throws Exception {
            PlaceOrderRequest orderRequest = new PlaceOrderRequest(
                    999999L,
                    1,
                    "789 Phantom Road, Nowhere"
            );

            mockMvc.perform(post("/api/orders")
                            .contentType(MediaType.APPLICATION_JSON)
                            .content(objectMapper.writeValueAsString(orderRequest)))
                    .andExpect(status().isNotFound())
                    .andExpect(jsonPath("$.status", is(404)))
                    .andExpect(jsonPath("$.error", is("Not Found")))
                    .andExpect(jsonPath("$.message", containsString("Product not found with id: 999999")));

            assertThat(orderRepository.count()).isEqualTo(0);
        }

        @Test
        @DisplayName("8. Negative Path: Place order with invalid quantity zero returns 400 Bad Request")
        void placeOrder_InvalidQuantityZero_Returns400() throws Exception {
            Product product = productRepository.save(new Product(
                    "Smart Thermostat",
                    "WiFi home thermostat",
                    new BigDecimal("120.00"),
                    10
            ));

            PlaceOrderRequest orderRequest = new PlaceOrderRequest(
                    product.getId(),
                    0, // Validation requires quantity >= 1
                    "100 Eco Blvd, Austin, TX"
            );

            mockMvc.perform(post("/api/orders")
                            .contentType(MediaType.APPLICATION_JSON)
                            .content(objectMapper.writeValueAsString(orderRequest)))
                    .andExpect(status().isBadRequest())
                    .andExpect(jsonPath("$.status", is(400)))
                    .andExpect(jsonPath("$.error", is("Validation Failed")))
                    .andExpect(jsonPath("$.errors.quantity", notNullValue()));

            assertThat(orderRepository.count()).isEqualTo(0);
        }

        @Test
        @DisplayName("9. Negative Path: Place order with blank shipping address returns 400 Bad Request")
        void placeOrder_BlankShippingAddress_Returns400() throws Exception {
            Product product = productRepository.save(new Product(
                    "Wireless Earbuds",
                    "Compact bluetooth buds",
                    new BigDecimal("49.99"),
                    15
            ));

            PlaceOrderRequest orderRequest = new PlaceOrderRequest(
                    product.getId(),
                    1,
                    "   " // Blank address
            );

            mockMvc.perform(post("/api/orders")
                            .contentType(MediaType.APPLICATION_JSON)
                            .content(objectMapper.writeValueAsString(orderRequest)))
                    .andExpect(status().isBadRequest())
                    .andExpect(jsonPath("$.status", is(400)))
                    .andExpect(jsonPath("$.error", is("Validation Failed")))
                    .andExpect(jsonPath("$.errors.shippingAddress", notNullValue()));

            assertThat(orderRepository.count()).isEqualTo(0);
        }
    }

    // =========================================================================
    // Scenario 3: Update an existing order
    // =========================================================================
    @Nested
    @DisplayName("Scenario 3: Update an Existing Order")
    class UpdateOrderTests {

        @Test
        @DisplayName("10. Happy Path: Update shipping address and status of existing order returns 200")
        void updateOrder_ValidAddressAndStatus_Returns200AndUpdatesState() throws Exception {
            Product product = productRepository.save(new Product("Gaming Mouse", "Wireless 16000 DPI", new BigDecimal("59.99"), 20));
            Order order = orderRepository.save(new Order(product.getId(), 2, new BigDecimal("119.98"), "Old Address 100", OrderStatus.CONFIRMED));

            UpdateOrderRequest updateRequest = new UpdateOrderRequest(
                    "New Address 200, Suite 5B",
                    OrderStatus.SHIPPED
            );

            mockMvc.perform(put("/api/orders/" + order.getId())
                            .contentType(MediaType.APPLICATION_JSON)
                            .content(objectMapper.writeValueAsString(updateRequest)))
                    .andExpect(status().isOk())
                    .andExpect(jsonPath("$.id", is(order.getId().intValue())))
                    .andExpect(jsonPath("$.shippingAddress", is("New Address 200, Suite 5B")))
                    .andExpect(jsonPath("$.status", is("SHIPPED")));

            Order updatedOrder = orderRepository.findById(order.getId()).orElseThrow();
            assertThat(updatedOrder.getShippingAddress()).isEqualTo("New Address 200, Suite 5B");
            assertThat(updatedOrder.getStatus()).isEqualTo(OrderStatus.SHIPPED);
        }

        @Test
        @DisplayName("11. Happy Path: Update only shipping address leaves status unchanged")
        void updateOrder_AddressOnly_Returns200AndPreservesStatus() throws Exception {
            Product product = productRepository.save(new Product("Desk Lamp", "LED dimmable lamp", new BigDecimal("29.99"), 15));
            Order order = orderRepository.save(new Order(product.getId(), 1, new BigDecimal("29.99"), "Initial Address 1", OrderStatus.CONFIRMED));

            UpdateOrderRequest updateRequest = new UpdateOrderRequest(
                    "Updated Address 500",
                    null // Status unchanged
            );

            mockMvc.perform(put("/api/orders/" + order.getId())
                            .contentType(MediaType.APPLICATION_JSON)
                            .content(objectMapper.writeValueAsString(updateRequest)))
                    .andExpect(status().isOk())
                    .andExpect(jsonPath("$.shippingAddress", is("Updated Address 500")))
                    .andExpect(jsonPath("$.status", is("CONFIRMED")));

            Order reloadedOrder = orderRepository.findById(order.getId()).orElseThrow();
            assertThat(reloadedOrder.getShippingAddress()).isEqualTo("Updated Address 500");
            assertThat(reloadedOrder.getStatus()).isEqualTo(OrderStatus.CONFIRMED);
        }

        @Test
        @DisplayName("12. Negative Path: Update non-existent order ID returns 404 Not Found")
        void updateOrder_NonExistentOrder_Returns404() throws Exception {
            UpdateOrderRequest updateRequest = new UpdateOrderRequest(
                    "Non-existent Street",
                    OrderStatus.SHIPPED
            );

            mockMvc.perform(put("/api/orders/999999")
                            .contentType(MediaType.APPLICATION_JSON)
                            .content(objectMapper.writeValueAsString(updateRequest)))
                    .andExpect(status().isNotFound())
                    .andExpect(jsonPath("$.status", is(404)))
                    .andExpect(jsonPath("$.error", is("Not Found")));
        }

        @Test
        @DisplayName("13. Negative Path: Update an order that is already CANCELLED returns 400 Bad Request")
        void updateOrder_AlreadyCancelled_Returns400() throws Exception {
            Product product = productRepository.save(new Product("USB-C Hub", "Multiport adapter", new BigDecimal("35.00"), 15));
            Order cancelledOrder = orderRepository.save(new Order(product.getId(), 1, new BigDecimal("35.00"), "789 Dock Rd", OrderStatus.CANCELLED));

            UpdateOrderRequest updateRequest = new UpdateOrderRequest(
                    "Attempted New Address",
                    OrderStatus.CONFIRMED
            );

            mockMvc.perform(put("/api/orders/" + cancelledOrder.getId())
                            .contentType(MediaType.APPLICATION_JSON)
                            .content(objectMapper.writeValueAsString(updateRequest)))
                    .andExpect(status().isBadRequest())
                    .andExpect(jsonPath("$.status", is(400)))
                    .andExpect(jsonPath("$.error", is("Bad Request")))
                    .andExpect(jsonPath("$.message", containsString("Cannot update order in CANCELLED status")));
        }

        @Test
        @DisplayName("14. Negative Path: Update an order that is already SHIPPED returns 400 Bad Request")
        void updateOrder_AlreadyShipped_Returns400() throws Exception {
            Product product = productRepository.save(new Product("Webcam 4K", "Ultra HD streaming cam", new BigDecimal("99.00"), 8));
            Order shippedOrder = orderRepository.save(new Order(product.getId(), 1, new BigDecimal("99.00"), "33 Sunset Blvd", OrderStatus.SHIPPED));

            UpdateOrderRequest updateRequest = new UpdateOrderRequest(
                    "Reroute Delivery Address",
                    OrderStatus.CANCELLED
            );

            mockMvc.perform(put("/api/orders/" + shippedOrder.getId())
                            .contentType(MediaType.APPLICATION_JSON)
                            .content(objectMapper.writeValueAsString(updateRequest)))
                    .andExpect(status().isBadRequest())
                    .andExpect(jsonPath("$.status", is(400)))
                    .andExpect(jsonPath("$.error", is("Bad Request")))
                    .andExpect(jsonPath("$.message", containsString("Cannot update order in SHIPPED status")));
        }

        @Test
        @DisplayName("15. State Transition & Inventory: Cancelling an order restores inventory back to the product")
        void updateOrder_CancelOrder_RestoresProductStock() throws Exception {
            // Start product with 10 units, order 3 units -> product stock is 7
            Product product = productRepository.save(new Product("Smart Watch", "Fitness tracker", new BigDecimal("150.00"), 7));
            Order confirmedOrder = orderRepository.save(new Order(product.getId(), 3, new BigDecimal("450.00"), "321 Running Track", OrderStatus.CONFIRMED));

            UpdateOrderRequest cancelRequest = new UpdateOrderRequest(
                    null,
                    OrderStatus.CANCELLED
            );

            mockMvc.perform(put("/api/orders/" + confirmedOrder.getId())
                            .contentType(MediaType.APPLICATION_JSON)
                            .content(objectMapper.writeValueAsString(cancelRequest)))
                    .andExpect(status().isOk())
                    .andExpect(jsonPath("$.status", is("CANCELLED")));

            // Assert that 3 units were restored to the product: 7 + 3 = 10
            Product reloadedProduct = productRepository.findById(product.getId()).orElseThrow();
            assertThat(reloadedProduct.getStock()).isEqualTo(10);
        }
    }
}
