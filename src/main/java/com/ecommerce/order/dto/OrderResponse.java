package com.ecommerce.order.dto;

import com.ecommerce.order.Order;
import com.ecommerce.order.OrderStatus;

import java.math.BigDecimal;
import java.time.Instant;

public record OrderResponse(
        Long id,
        Long productId,
        Integer quantity,
        BigDecimal totalAmount,
        String shippingAddress,
        OrderStatus status,
        Instant createdAt
) {
    public static OrderResponse fromEntity(Order order) {
        return new OrderResponse(
                order.getId(),
                order.getProductId(),
                order.getQuantity(),
                order.getTotalAmount(),
                order.getShippingAddress(),
                order.getStatus(),
                order.getCreatedAt()
        );
    }
}
