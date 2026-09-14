package com.ecommerce.order;

import java.math.BigDecimal;
import java.time.Instant;

import org.junit.jupiter.api.BeforeEach;
import org.mockito.Mockito;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.web.servlet.MockMvc;

import com.ecommerce.ECommerceApplication;
import com.ecommerce.order.dto.OrderResponse;
import com.ecommerce.order.dto.PlaceOrderRequest;
import com.ecommerce.order.dto.UpdateOrderRequest;

import io.restassured.module.mockmvc.RestAssuredMockMvc;

@SpringBootTest(classes = ECommerceApplication.class)
@AutoConfigureMockMvc
public abstract class OrderBaseClass {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private OrderService orderService;

    @BeforeEach
    public void setup() {
        RestAssuredMockMvc.mockMvc(mockMvc);

        Instant fixedTimestamp = Instant.parse("2026-09-14T15:00:00Z");

        OrderResponse createdResponse = new OrderResponse(
                100L,
                1L,
                2,
                new BigDecimal("49.98"),
                "123 Main Street",
                OrderStatus.PENDING,
                fixedTimestamp
        );
        Mockito.when(orderService.placeOrder(Mockito.any(PlaceOrderRequest.class)))
                .thenReturn(createdResponse);

        OrderResponse updatedResponse = new OrderResponse(
                100L,
                1L,
                2,
                new BigDecimal("49.98"),
                "123 Main Street",
                OrderStatus.SHIPPED,
                fixedTimestamp
        );
        Mockito.when(orderService.updateOrder(Mockito.eq(100L), Mockito.any(UpdateOrderRequest.class)))
                .thenReturn(updatedResponse);
    }
}