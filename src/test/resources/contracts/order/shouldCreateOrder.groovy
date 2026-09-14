package contracts.order

import org.springframework.cloud.contract.spec.Contract

Contract.make {
    description "Should place a new order successfully"

    request {
        method POST()
        url '/api/orders'
        headers {
            contentType(applicationJson())
        }
        body([
            productId: 1,
            quantity: 2,
            shippingAddress: "123 Main Street"
        ])
    }

    response {
        status CREATED()
        headers {
            contentType(applicationJson())
        }
        body([
            id: 100,
            productId: 1,
            quantity: 2,
            totalAmount: 49.98,
            shippingAddress: "123 Main Street",
            status: "PENDING",
            createdAt: "2026-09-14T15:00:00Z"
        ])
    }
}