# ==========================================
# Stage 1: Build Stage
# ==========================================
FROM maven:3.9-eclipse-temurin-21-alpine AS builder

WORKDIR /app

# Cache dependencies first by copying only pom.xml
COPY pom.xml .
RUN mvn dependency:go-offline -B

# Copy source code and build production jar
COPY src ./src
RUN mvn clean package -DskipTests -B

# ==========================================
# Stage 2: Minimal Runtime Stage
# ==========================================
FROM eclipse-temurin:21-jre-alpine AS runner

WORKDIR /app

# Run as non-privileged user for container security
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Copy compiled jar from build stage
COPY --from=builder /app/target/ecommerce-service-1.0.0.jar app.jar
RUN chown appuser:appgroup app.jar

USER appuser

EXPOSE 8080

# Healthcheck to monitor service readiness
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:8080/api/products || exit 1

ENTRYPOINT ["java", "-XX:+UseContainerSupport", "-XX:MaxRAMPercentage=75.0", "-jar", "app.jar"]
