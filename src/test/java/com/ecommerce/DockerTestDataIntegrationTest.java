package com.ecommerce;

import com.ecommerce.order.Order;
import com.ecommerce.order.OrderRepository;
import com.ecommerce.order.OrderStatus;
import com.ecommerce.order.dto.PlaceOrderRequest;
import com.ecommerce.product.Product;
import com.ecommerce.product.ProductRepository;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.condition.EnabledIf;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.MvcResult;

import java.net.Socket;
import java.util.Optional;

import static org.assertj.core.api.Assertions.assertThat;
import static org.hamcrest.Matchers.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

/**
 * Task 3: Test Data Management in Docker
 * Demonstrates running integration tests against containerized PostgreSQL test data.
 * Executes automatically when the Docker test-db container is active on port 5433.
 */
@SpringBootTest
@AutoConfigureMockMvc
@ActiveProfiles("docker")
@EnabledIf("isDockerTestDbAvailable")
class DockerTestDataIntegrationTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @Autowired
    private ProductRepository productRepository;

    @Autowired
    private OrderRepository orderRepository;

    static boolean isDockerTestDbAvailable() {
        try (Socket socket = new Socket("localhost", 5433)) {
            return true;
        } catch (Exception e) {
            return false;
        }
    }

    @Test
    @DisplayName("Verify pre-seeded bakery test data exists in Docker PostgreSQL (Cookies & Pastries in PHP)")
    void testPreSeededDataInDockerDatabase() throws Exception {
        // Query the Docker PostgreSQL database for the baseline bakery product seeded by init-test-data.sql
        mockMvc.perform(get("/api/v1/items"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$", not(empty())))
                .andExpect(jsonPath("$[*].name", hasItem("Chocolate Chip Cookie Box")));
    }

    @Test
    @DisplayName("Place pastry order against Docker test database and verify PHP total amount and stock deduction")
    void testPlaceOrderAgainstDockerContainerDatabase() throws Exception {
        // Find the seeded product 'Chocolate Chip Cookie Box' (PHP 250.00 each, 20 in stock)
        Optional<Product> cookieOpt = productRepository.findAll().stream()
                .filter(p -> p.getName().equals("Chocolate Chip Cookie Box"))
                .findFirst();

        assertThat(cookieOpt).isPresent();
        Product cookieBox = cookieOpt.get();
        int initialStock = cookieBox.getStock();

        PlaceOrderRequest orderRequest = new PlaceOrderRequest(
                cookieBox.getId(),
                2,
                "Unit 4B, BGC High Street, Taguig City, Metro Manila"
        );

        MvcResult result = mockMvc.perform(post("/api/orders")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(orderRequest)))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.productId", is(cookieBox.getId().intValue())))
                .andExpect(jsonPath("$.quantity", is(2)))
                .andExpect(jsonPath("$.totalAmount", is(500.00))) // PHP 250.00 * 2 = PHP 500.00
                .andExpect(jsonPath("$.status", is("CONFIRMED")))
                .andReturn();

        Long orderId = objectMapper.readTree(result.getResponse().getContentAsString()).get("id").asLong();

        // Verify order is saved in the real Docker PostgreSQL database
        Order savedOrder = orderRepository.findById(orderId).orElse(null);
        assertThat(savedOrder).isNotNull();
        assertThat(savedOrder.getShippingAddress()).isEqualTo("Unit 4B, BGC High Street, Taguig City, Metro Manila");
        assertThat(savedOrder.getTotalAmount()).isEqualByComparingTo("500.00");

        // Verify stock is decremented in Docker PostgreSQL (20 - 2 = 18)
        Product updatedCookieBox = productRepository.findById(cookieBox.getId()).orElseThrow();
        assertThat(updatedCookieBox.getStock()).isEqualTo(initialStock - 2);
    }
}
