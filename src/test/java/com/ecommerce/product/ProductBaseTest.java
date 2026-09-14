package com.ecommerce.product;

import java.math.BigDecimal;

import org.junit.jupiter.api.BeforeEach;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.web.context.WebApplicationContext;

import com.ecommerce.ECommerceApplication;

import io.restassured.module.mockmvc.RestAssuredMockMvc;

@SpringBootTest(classes = ECommerceApplication.class)
// @SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.MOCK)
public abstract class ProductBaseTest {

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