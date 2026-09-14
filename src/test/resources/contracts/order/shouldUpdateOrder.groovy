package contracts.order

import org.springframework.cloud.contract.spec.Contract

Contract.make {
    description "Should update an existing order status"

    request {
        method PUT()
        url '/api/orders/100'
        headers {
            contentType(applicationJson())
        }
        body([
            shippingAddress: "123 Main Street",
            status: "SHIPPED"
        ])
    }

    response {
        status OK()
        headers {
            contentType(applicationJson())
        }
        body([
            id: 100,
            productId: 1,
            quantity: 2,
            totalAmount: 49.98,
            shippingAddress: "123 Main Street",
            status: "SHIPPED",
            createdAt: "2026-09-14T15:00:00Z"
        ])
    }
}