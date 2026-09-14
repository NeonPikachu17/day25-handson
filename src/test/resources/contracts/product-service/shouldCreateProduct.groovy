org.springframework.cloud.contract.spec.Contract.make {
    request {
        method 'POST'
        url '/api/products'
        headers {
            contentType('application/json')
        }
        body([
            name: 'New Gadget',
            description: 'An innovative gadget',
            price: 150.00,
            stock: 25
        ])
    }
    response {
        status 201
        headers {
            contentType('application/json')
        }
        body([
            id: $(anyNumber()),
            name: 'New Gadget',
            description: 'An innovative gadget',
            price: 150.00,
            stock: 25
        ])
    }
}