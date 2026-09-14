package com.ecommerce.product;

import com.ecommerce.AbstractContainerIntegrationTest;
import io.restassured.module.mockmvc.RestAssuredMockMvc;
import org.junit.jupiter.api.BeforeEach;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.context.WebApplicationContext;

import java.math.BigDecimal;

public abstract class ProductBaseTest extends AbstractContainerIntegrationTest {

    @Autowired
    private WebApplicationContext context;

    @Autowired
    private ProductRepository productRepository;

    @BeforeEach
    public void setup() {
        RestAssuredMockMvc.webAppContextSetup(context);
        
        // Reset database and seed product with ID 1
        productRepository.deleteAll();
        Product sampleProduct = new Product(
            "Sample Product",
            "A test product description",
            new BigDecimal("99.99"),
            10
        );
        productRepository.save(sampleProduct);
    }
}