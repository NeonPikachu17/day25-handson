package com.ecommerce.order.dto;

import com.ecommerce.order.OrderStatus;

public record UpdateOrderRequest(
        String shippingAddress,
        OrderStatus status
) {
}
