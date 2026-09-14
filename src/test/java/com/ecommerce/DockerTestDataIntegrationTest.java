package com.ecommerce;

import com.ecommerce.factory.ProductFactory;
import com.ecommerce.order.Order;
import com.ecommerce.order.OrderRepository;
import com.ecommerce.order.dto.PlaceOrderRequest;
import com.ecommerce.product.Product;
import com.ecommerce.product.ProductRepository;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MvcResult;

import static org.assertj.core.api.Assertions.assertThat;
import static org.hamcrest.Matchers.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

/**
 * Task 3: Test Data Management in Containerized PostgreSQL
 * Validates:
 * 1. Throwaway PostgreSQL container automatically launched via Testcontainers.
 * 2. Database dynamic ports bind seamlessly.
 * 3. Schema migrations (Flyway) auto-apply on container startup.
 * 4. Programmatic entity factories deliver valid Product & Order objects.
 * 5. Database state resets via table truncation hooks.
 */
class DockerTestDataIntegrationTest extends AbstractContainerIntegrationTest {

    @Autowired
    private ProductRepository productRepository;

    @Autowired
    private OrderRepository orderRepository;

    @Test
    @DisplayName("Verify bakery products delivered via ProductFactory in PostgreSQL container (PHP Currency)")
    void testPreSeededDataInDockerDatabase() throws Exception {
        productRepository.save(ProductFactory.createValidProduct());
        productRepository.save(ProductFactory.createUbePandesal());
        productRepository.save(ProductFactory.createCroissant());

        mockMvc.perform(get("/api/v1/items"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$", hasSize(3)))
                .andExpect(jsonPath("$[0].name", is("Chocolate Chip Cookie Box")))
                .andExpect(jsonPath("$[0].price", is(250.00)))
                .andExpect(jsonPath("$[1].name", is("Ube Cheese Pandesal")))
                .andExpect(jsonPath("$[1].price", is(180.00)));
    }

    @Test
    @DisplayName("Place pastry order against throwaway container and verify PHP total amount and stock deduction")
    void testPlaceOrderAgainstDockerContainerDatabase() throws Exception {
        Product cookieBox = productRepository.save(ProductFactory.createValidProduct());
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

        // Verify stock is decremented in container PostgreSQL (20 - 2 = 18)
        Product updatedCookieBox = productRepository.findById(cookieBox.getId()).orElseThrow();
        assertThat(updatedCookieBox.getStock()).isEqualTo(initialStock - 2);
    }
}
