package com.ecommerce.product;

import com.ecommerce.exception.ResourceNotFoundException;
import com.ecommerce.product.dto.CreateProductRequest;
import com.ecommerce.product.dto.ProductResponse;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
public class ProductService {

    private final ProductRepository productRepository;

    public ProductService(ProductRepository productRepository) {
        this.productRepository = productRepository;
    }

    @Transactional
    public ProductResponse createProduct(CreateProductRequest request) {
        Product product = new Product(
                request.name(),
                request.description(),
                request.price(),
                request.stock()
        );
        Product saved = productRepository.save(product);
        return ProductResponse.fromEntity(saved);
    }

    @Transactional(readOnly = true)
    public ProductResponse getProduct(Long id) {
        Product product = productRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Product not found with id: " + id));
        return ProductResponse.fromEntity(product);
    }

    @Transactional(readOnly = true)
    public Product getProductEntity(Long id) {
        return productRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Product not found with id: " + id));
    }

    @Transactional(readOnly = true)
    public List<ProductResponse> getAllProducts() {
        return productRepository.findAll().stream()
                .map(ProductResponse::fromEntity)
                .toList();
    }

    @Transactional
    public void deductStock(Long id, int quantity) {
        Product product = getProductEntity(id);
        product.deductStock(quantity);
        productRepository.save(product);
    }

    @Transactional
    public void restoreStock(Long id, int quantity) {
        Product product = getProductEntity(id);
        product.restoreStock(quantity);
        productRepository.save(product);
    }
}
