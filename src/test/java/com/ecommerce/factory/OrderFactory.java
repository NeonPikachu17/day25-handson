package com.ecommerce.factory;

import com.ecommerce.order.Order;
import com.ecommerce.order.OrderStatus;
import com.ecommerce.product.Product;
import java.math.BigDecimal;

/**
 * Programmatic entity factory delivering valid Order instances for test setups.
 * Fulfills Acceptance Criterion: Programmatic entity factories deliver valid Order objects.
 */
public class OrderFactory {

    public static Order createValidOrder(Product product, int quantity) {
        BigDecimal total = product.getPrice().multiply(BigDecimal.valueOf(quantity));
        return new Order(
                product.getId(),
                quantity,
                total,
                "Unit 12B, Katipunan Avenue, Quezon City, Metro Manila",
                OrderStatus.CONFIRMED
        );
    }

    public static Order createOrderWithStatus(Product product, int quantity, OrderStatus status) {
        BigDecimal total = product.getPrice().multiply(BigDecimal.valueOf(quantity));
        return new Order(
                product.getId(),
                quantity,
                total,
                "Unit 4B, BGC High Street, Taguig City, Metro Manila",
                status
        );
    }

    public static Order createCancelledOrder(Product product) {
        return createOrderWithStatus(product, 1, OrderStatus.CANCELLED);
    }

    public static Order createShippedOrder(Product product) {
        return createOrderWithStatus(product, 1, OrderStatus.SHIPPED);
    }

    public static Builder builder() {
        return new Builder();
    }

    public static class Builder {
        private Long productId = 1L;
        private int quantity = 1;
        private BigDecimal totalAmount = new BigDecimal("250.00");
        private String shippingAddress = "Unit 12B, Katipunan Avenue, Quezon City, Metro Manila";
        private OrderStatus status = OrderStatus.CONFIRMED;

        public Builder withProductId(Long productId) {
            this.productId = productId;
            return this;
        }

        public Builder withQuantity(int quantity) {
            this.quantity = quantity;
            return this;
        }

        public Builder withTotalAmount(BigDecimal totalAmount) {
            this.totalAmount = totalAmount;
            return this;
        }

        public Builder withShippingAddress(String shippingAddress) {
            this.shippingAddress = shippingAddress;
            return this;
        }

        public Builder withStatus(OrderStatus status) {
            this.status = status;
            return this;
        }

        public Order build() {
            return new Order(productId, quantity, totalAmount, shippingAddress, status);
        }
    }
}
