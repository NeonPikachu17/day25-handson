package com.ecommerce.order;

import com.ecommerce.exception.ResourceNotFoundException;
import com.ecommerce.order.dto.OrderResponse;
import com.ecommerce.order.dto.PlaceOrderRequest;
import com.ecommerce.order.dto.UpdateOrderRequest;
import com.ecommerce.product.Product;
import com.ecommerce.product.ProductService;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.util.List;

@Service
public class OrderService {

    private final OrderRepository orderRepository;
    private final ProductService productService;

    public OrderService(OrderRepository orderRepository, ProductService productService) {
        this.orderRepository = orderRepository;
        this.productService = productService;
    }

    @Transactional
    public OrderResponse placeOrder(PlaceOrderRequest request) {
        Product product = productService.getProductEntity(request.productId());

        // Deduct inventory (throws InsufficientStockException if stock < quantity)
        productService.deductStock(product.getId(), request.quantity());

        BigDecimal totalAmount = product.getPrice().multiply(BigDecimal.valueOf(request.quantity()));

        Order order = new Order(
                product.getId(),
                request.quantity(),
                totalAmount,
                request.shippingAddress(),
                OrderStatus.CONFIRMED
        );

        Order saved = orderRepository.save(order);
        return OrderResponse.fromEntity(saved);
    }

    @Transactional
    public OrderResponse updateOrder(Long orderId, UpdateOrderRequest request) {
        Order order = orderRepository.findById(orderId)
                .orElseThrow(() -> new ResourceNotFoundException("Order not found with id: " + orderId));

        // Negative check: Prevent updating orders that are already in terminal state
        if (order.getStatus() == OrderStatus.CANCELLED || order.getStatus() == OrderStatus.SHIPPED) {
            throw new IllegalStateException("Cannot update order in " + order.getStatus() + " status");
        }

        // Handle status update
        if (request.status() != null && request.status() != order.getStatus()) {
            if (request.status() == OrderStatus.CANCELLED) {
                // Restore stock when order is cancelled
                productService.restoreStock(order.getProductId(), order.getQuantity());
            }
            order.setStatus(request.status());
        }

        // Handle address update
        if (request.shippingAddress() != null && !request.shippingAddress().isBlank()) {
            order.setShippingAddress(request.shippingAddress().trim());
        }

        Order updated = orderRepository.save(order);
        return OrderResponse.fromEntity(updated);
    }

    @Transactional(readOnly = true)
    public OrderResponse getOrder(Long orderId) {
        Order order = orderRepository.findById(orderId)
                .orElseThrow(() -> new ResourceNotFoundException("Order not found with id: " + orderId));
        return OrderResponse.fromEntity(order);
    }

    @Transactional(readOnly = true)
    public List<OrderResponse> getAllOrders() {
        return orderRepository.findAll().stream()
                .map(OrderResponse::fromEntity)
                .toList();
    }
}
