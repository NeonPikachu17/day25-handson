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
    @DisplayName("Verify pre-seeded baseline test data exists in Docker PostgreSQL")
    void testPreSeededDataInDockerDatabase() throws Exception {
        // Query the Docker PostgreSQL database for the baseline product seeded by init-test-data.sql
        mockMvc.perform(get("/api/products"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$", not(empty())))
                .andExpect(jsonPath("$[*].name", hasItem("Test Gaming Laptop")));
    }

    @Test
    @DisplayName("Place order against Docker test database and verify persistence in container")
    void testPlaceOrderAgainstDockerContainerDatabase() throws Exception {
        // Find the seeded product 'Test Gaming Laptop'
        Optional<Product> laptopOpt = productRepository.findAll().stream()
                .filter(p -> p.getName().equals("Test Gaming Laptop"))
                .findFirst();

        assertThat(laptopOpt).isPresent();
        Product laptop = laptopOpt.get();
        int initialStock = laptop.getStock();

        PlaceOrderRequest orderRequest = new PlaceOrderRequest(
                laptop.getId(),
                2,
                "999 Docker Container Way, Suite 10"
        );

        MvcResult result = mockMvc.perform(post("/api/orders")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(orderRequest)))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.productId", is(laptop.getId().intValue())))
                .andExpect(jsonPath("$.quantity", is(2)))
                .andExpect(jsonPath("$.status", is("CONFIRMED")))
                .andReturn();

        Long orderId = objectMapper.readTree(result.getResponse().getContentAsString()).get("id").asLong();

        // Verify order is saved in the real Docker PostgreSQL database
        Order savedOrder = orderRepository.findById(orderId).orElse(null);
        assertThat(savedOrder).isNotNull();
        assertThat(savedOrder.getShippingAddress()).isEqualTo("999 Docker Container Way, Suite 10");

        // Verify stock is decremented in Docker PostgreSQL
        Product updatedLaptop = productRepository.findById(laptop.getId()).orElseThrow();
        assertThat(updatedLaptop.getStock()).isEqualTo(initialStock - 2);
    }
}
