org.springframework.cloud.contract.spec.Contract.make {
    request {
        method 'GET'
        url '/api/products/1'
    }
    response {
        status 200
        headers {
            contentType('application/json')
        }
        body([
            id: 1,
            name: 'Sample Product',
            description: 'A test product description',
            price: 99.99,
            stock: 10
        ])
    }
}