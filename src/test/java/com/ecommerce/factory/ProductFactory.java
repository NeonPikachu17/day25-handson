package com.ecommerce.factory;

import com.ecommerce.product.Product;
import java.math.BigDecimal;

/**
 * Programmatic entity factory delivering valid Product instances for test setups.
 * Fulfills Acceptance Criterion: Programmatic entity factories deliver valid Product objects.
 */
public class ProductFactory {

    public static Product createValidProduct() {
        return new Product(
                "Chocolate Chip Cookie Box",
                "Freshly baked artisan cookies with Belgian chocolate chips - Box of 6 (PHP 250.00)",
                new BigDecimal("250.00"),
                20
        );
    }

    public static Product createUbePandesal() {
        return new Product(
                "Ube Cheese Pandesal",
                "Soft bakery pastry filled with creamy ube halaya and savory cheese - Box of 10 (PHP 180.00)",
                new BigDecimal("180.00"),
                50
        );
    }

    public static Product createCroissant() {
        return new Product(
                "Matcha Cream Croissant",
                "Flaky French butter croissant infused with Japanese Uji matcha cream (PHP 140.00)",
                new BigDecimal("140.00"),
                10
        );
    }

    public static Product createCustomProduct(String name, String description, BigDecimal price, int stock) {
        return new Product(name, description, price, stock);
    }

    public static Builder builder() {
        return new Builder();
    }

    public static class Builder {
        private String name = "Chocolate Chip Cookie Box";
        private String description = "Freshly baked artisan cookies - Box of 6 (PHP 250.00)";
        private BigDecimal price = new BigDecimal("250.00");
        private int stock = 20;

        public Builder withName(String name) {
            this.name = name;
            return this;
        }

        public Builder withDescription(String description) {
            this.description = description;
            return this;
        }

        public Builder withPrice(BigDecimal price) {
            this.price = price;
            return this;
        }

        public Builder withStock(int stock) {
            this.stock = stock;
            return this;
        }

        public Product build() {
            return new Product(name, description, price, stock);
        }
    }
}
