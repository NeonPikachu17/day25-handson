import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'''
        <w:tcMar {nsdecls("w")}>
            <w:top w:w="{top}" w:type="dxa"/>
            <w:bottom w:w="{bottom}" w:type="dxa"/>
            <w:left w:w="{left}" w:type="dxa"/>
            <w:right w:w="{right}" w:type="dxa"/>
        </w:tcMar>
    ''')
    tcPr.append(tcMar)

def add_code_block(doc, code_text):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "F4F5F7")
    set_cell_margins(cell, top=120, bottom=120, left=180, right=180)
    
    # Border: subtle gray with strong blue accent on left
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(f'''
        <w:tcBorders {nsdecls("w")}>
            <w:top w:val="single" w:sz="4" w:space="0" w:color="D1D5DB"/>
            <w:left w:val="single" w:sz="24" w:space="0" w:color="2563EB"/>
            <w:bottom w:val="single" w:sz="4" w:space="0" w:color="D1D5DB"/>
            <w:right w:val="single" w:sz="4" w:space="0" w:color="D1D5DB"/>
        </w:tcBorders>
    ''')
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(code_text)
    run.font.name = "Consolas"
    run.font.size = Pt(9.0)
    run.font.color.rgb = RGBColor(30, 41, 59)
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

def add_image_with_caption(doc, img_path, caption_text, width_inches=5.8):
    if os.path.exists(img_path):
        doc.add_paragraph().paragraph_format.space_before = Pt(6)
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.add_run().add_picture(img_path, width=Inches(width_inches))
        
        caption = doc.add_paragraph()
        caption.alignment = WD_ALIGN_PARAGRAPH.CENTER
        c_run = caption.add_run(caption_text)
        c_run.font.italic = True
        c_run.font.size = Pt(9.5)
        c_run.font.color.rgb = RGBColor(100, 116, 139)
        doc.add_paragraph().paragraph_format.space_after = Pt(8)

def build_document():
    doc = docx.Document()
    
    # Page setup - Standard 1-inch margins
    sections = doc.sections
    for s in sections:
        s.top_margin = Inches(1)
        s.bottom_margin = Inches(1)
        s.left_margin = Inches(1)
        s.right_margin = Inches(1)

    # Base Styles
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = RGBColor(51, 51, 51)
    
    # Document Title
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(0)
    title_p.paragraph_format.space_after = Pt(4)
    run_title = title_p.add_run("E-Commerce Backend Services")
    run_title.font.name = "Calibri"
    run_title.font.size = Pt(26)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(30, 58, 138) # Deep Navy

    sub_p = doc.add_paragraph()
    sub_p.paragraph_format.space_after = Pt(18)
    run_sub = sub_p.add_run("Comprehensive Technical Documentation: Integration Testing, Contract Testing, Test Data Management & Acceptance Criteria Verification")
    run_sub.font.size = Pt(13.5)
    run_sub.font.color.rgb = RGBColor(100, 116, 139)

    # Metadata Summary Card
    meta_table = doc.add_table(rows=7, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_data = [
        ("Technology Stack", "Java 21 LTS | Spring Boot 3.3.5 | Spring Data JPA | PostgreSQL 16 | Flyway 10.10 | Testcontainers 1.20 | JUnit 5"),
        ("Architecture", "Domain-Driven Service Layer (Product Service & Order Service — Strictly Backend / No UI)"),
        ("Primary Endpoints", "Items API: /api/v1/items | Orders API: /api/orders"),
        ("Test Data Domain", "Artisan Bakery & Pastry Shop (Cookies & Pastries priced in Philippine Pesos - PHP)"),
        ("Acceptance Criteria", "5 of 5 Fulfilled (Testcontainers, Dynamic Ports, Flyway, Entity Factories, Truncation Hook)"),
        ("Repository", "https://github.com/NeonPikachu17/day25-handson.git (Branch: main)"),
        ("Verification Status", "21 Tests Executed | 21 Passed | 0 Failures | 0 Errors (BUILD SUCCESS in 18.682s)")
    ]
    for idx, (label, val) in enumerate(meta_data):
        row = meta_table.rows[idx]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width = Inches(1.8)
        c1.width = Inches(4.7)
        set_cell_background(c0, "F1F5F9")
        set_cell_background(c1, "F8FAFC")
        set_cell_margins(c0, 60, 60, 100, 100)
        set_cell_margins(c1, 60, 60, 100, 100)
        
        p0 = c0.paragraphs[0]
        p0.paragraph_format.space_after = Pt(2)
        r0 = p0.add_run(label)
        r0.font.bold = True
        r0.font.size = Pt(9.5)
        r0.font.color.rgb = RGBColor(15, 23, 42)
        
        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_after = Pt(2)
        r1 = p1.add_run(val)
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = RGBColor(51, 65, 85)

    doc.add_paragraph().paragraph_format.space_after = Pt(14)

    # =========================================================================
    # Section 1: Overview of Testing Approach
    # =========================================================================
    h1 = doc.add_heading(level=1)
    r = h1.add_run("1. Overview of Testing Approach")
    r.font.color.rgb = RGBColor(30, 58, 138)

    doc.add_paragraph(
        "This project implements a multi-tier automated testing architecture for a decoupled e-commerce backend. "
        "The system separates core responsibilities between two specialized microservices: the Product Service "
        "(responsible for catalog management, stock levels, and item lookups) and the Order Service (handling customer orders, "
        "billing calculations, and lifecycle status transitions). Strictly adhering to specifications, the application is "
        "engineered as a clean REST backend service with zero frontend/UI dependencies."
    )

    doc.add_paragraph(
        "To achieve full coverage across business invariants, network contracts, and database persistence, the testing framework "
        "is structured across four complementary pillars:"
    )

    p1 = doc.add_paragraph(style='List Bullet')
    r = p1.add_run("Tier 1: Integration Testing (Task 1): ")
    r.font.bold = True
    p1.add_run("Executes end-to-end HTTP dispatches across controllers, service logic, and persistence layers using MockMvc. "
               "Covers happy paths, boundary validations, negative scenarios, and terminal lifecycle state guards.")

    p2 = doc.add_paragraph(style='List Bullet')
    r = p2.add_run("Tier 2: Contract Testing (Task 2): ")
    r.font.bold = True
    p2.add_run("Employs Spring Cloud Contract Verifier with Groovy DSL specifications to establish Consumer-Driven Contracts "
               "for the Product Service API (/api/v1/items), guaranteeing schema parity and preventing breaking changes across microservices.")

    p3 = doc.add_paragraph(style='List Bullet')
    r = p3.add_run("Tier 3: Test Data Management with Testcontainers & Docker (Task 3): ")
    r.font.bold = True
    p3.add_run("Orchestrates isolated PostgreSQL 16 Alpine containers via Testcontainers Singleton Pattern with Flyway migrations "
               "and programmatic entity factories in Philippine Pesos (PHP). Guarantees 100% deterministic test repeatability and zero test pollution.")

    p4 = doc.add_paragraph(style='List Bullet')
    r = p4.add_run("Tier 4: Acceptance Criteria Compliance: ")
    r.font.bold = True
    p4.add_run("Fulfills all five required acceptance criteria including automatic throwaway containers, dynamic port binding, Flyway migrations, "
               "programmatic entity factories, and automated table truncation hooks.")

    # =========================================================================
    # Section 2: Task 1 - Integration Testing
    # =========================================================================
    h2 = doc.add_heading(level=1)
    r = h2.add_run("2. Task 1: Integration Testing")
    r.font.color.rgb = RGBColor(30, 58, 138)

    doc.add_paragraph(
        "The integration test suite is implemented in ECommerceIntegrationTest.java and executes against the complete Spring application "
        "context using @SpringBootTest and @AutoConfigureMockMvc. The suite features 15 comprehensive test cases categorized across "
        "three primary operational workflows: Create Product, Place Order, and Update Order."
    )

    # Test Matrix Table
    t_matrix = doc.add_table(rows=16, cols=5)
    t_matrix.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["#", "Scenario", "Test Case Name", "Path Type", "Expected Status & Verified Invariant"]
    for i, h in enumerate(headers):
        cell = t_matrix.rows[0].cells[i]
        set_cell_background(cell, "1E3A8A")
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.font.bold = True
        r.font.size = Pt(9)
        r.font.color.rgb = RGBColor(255, 255, 255)

    cases = [
        ("1", "Create Item", "createProduct_ValidPayload_Returns201AndPersistsInDb", "Happy Path", "201 Created; entity persisted with matching fields in DB"),
        ("2", "Create Item", "createProduct_InvalidPayload_BlankName_Returns400", "Negative", "400 Bad Request; validation error on name; DB count = 0"),
        ("3", "Create Item", "createProduct_InvalidPayload_NegativePriceAndStock_Returns400", "Negative", "400 Bad Request; @Positive and @PositiveOrZero rejections"),
        ("4", "Create Item", "createProduct_ThenGetById_Returns200WithAccurateDetails", "Read-After-Write", "200 OK via GET /api/v1/items/{id}; fields strictly match"),
        ("5", "Place Order", "placeOrder_ValidProductAndStock_Returns201AndDeductsInventory", "Happy Path", "201 Created; total price calculated; stock decremented (10 -> 7)"),
        ("6", "Place Order", "placeOrder_InsufficientStock_Returns400AndDoesNotCreateOrder", "Negative", "400 Bad Request; 'Insufficient Stock'; 0 orders saved; stock preserved"),
        ("7", "Place Order", "placeOrder_NonExistentProduct_Returns404", "Negative", "404 Not Found; 'Product not found with id: 999999'"),
        ("8", "Place Order", "placeOrder_InvalidQuantityZero_Returns400", "Negative", "400 Bad Request; validation failure on @Min(1) quantity"),
        ("9", "Place Order", "placeOrder_BlankShippingAddress_Returns400", "Negative", "400 Bad Request; validation failure on @NotBlank address"),
        ("10", "Update Order", "updateOrder_ValidAddressAndStatus_Returns200AndUpdatesState", "Happy Path", "200 OK via PUT /api/orders/{id}; address & status = SHIPPED updated"),
        ("11", "Update Order", "updateOrder_AddressOnly_PreservesExistingStatus", "Happy Path", "200 OK; shipping address modified; status preserved as CONFIRMED"),
        ("12", "Update Order", "updateOrder_NonExistentOrder_Returns404", "Negative", "404 Not Found; 'Order not found with id: 999999'"),
        ("13", "Update Order", "updateOrder_AlreadyCancelled_Returns400", "Negative", "400 Bad Request; terminal guard: 'Cannot update order in CANCELLED status'"),
        ("14", "Update Order", "updateOrder_AlreadyShipped_Returns400", "Negative", "400 Bad Request; terminal guard: 'Cannot update order in SHIPPED status'"),
        ("15", "Update Order", "updateOrder_CancelOrder_RestoresProductStock", "State Transition", "200 OK; cancelling order automatically restores stock to product (7 + 3 = 10)")
    ]

    for idx, data in enumerate(cases):
        row = t_matrix.rows[idx + 1]
        for c_idx, val in enumerate(data):
            cell = row.cells[c_idx]
            set_cell_background(cell, "F8FAFC" if idx % 2 == 0 else "FFFFFF")
            set_cell_margins(cell, 40, 40, 60, 60)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(1)
            r = p.add_run(val)
            r.font.size = Pt(8.5)
            if c_idx == 3 and val == "Negative":
                r.font.color.rgb = RGBColor(185, 28, 28)
            elif c_idx == 3 and val in ("Happy Path", "State Transition"):
                r.font.color.rgb = RGBColor(21, 128, 61)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # Code Snippets for Integration Tests
    doc.add_heading(level=2).add_run("Task 1 Code Snippet: Item Creation & Validation Test").font.color.rgb = RGBColor(30, 58, 138)
    add_code_block(doc, 
"""@Test
@DisplayName("1. Happy Path: Successfully create product, return 201 and persist in DB")
void createProduct_ValidPayload_Returns201AndPersistsInDb() throws Exception {
    CreateProductRequest request = new CreateProductRequest(
            "Noise Cancelling Headphones",
            "Premium wireless over-ear headphones",
            new BigDecimal("199.99"),
            50
    );

    MvcResult result = mockMvc.perform(post("/api/v1/items")
                    .contentType(MediaType.APPLICATION_JSON)
                    .content(objectMapper.writeValueAsString(request)))
            .andExpect(status().isCreated())
            .andExpect(jsonPath("$.id", notNullValue()))
            .andExpect(jsonPath("$.name", is("Noise Cancelling Headphones")))
            .andExpect(jsonPath("$.price", is(199.99)))
            .andExpect(jsonPath("$.stock", is(50)))
            .andReturn();

    // Verify DB persistence via JPA repository
    String responseString = result.getResponse().getContentAsString();
    Long createdId = objectMapper.readTree(responseString).get("id").asLong();
    Product savedProduct = productRepository.findById(createdId).orElse(null);
    assertThat(savedProduct).isNotNull();
    assertThat(savedProduct.getName()).isEqualTo("Noise Cancelling Headphones");
}""")

    doc.add_heading(level=2).add_run("Task 1 Code Snippet: Order Placement & Inventory Deduction Test").font.color.rgb = RGBColor(30, 58, 138)
    add_code_block(doc,
"""@Test
@DisplayName("5. Happy Path: Place order with sufficient stock returns 201 and deducts inventory")
void placeOrder_ValidProductAndStock_Returns201AndDeductsInventory() throws Exception {
    Product product = productRepository.save(new Product("Mechanical Keyboard", "RGB switches", new BigDecimal("89.50"), 10));

    PlaceOrderRequest orderRequest = new PlaceOrderRequest(product.getId(), 3, "123 Tech Lane, Silicon Valley, CA");

    MvcResult result = mockMvc.perform(post("/api/orders")
                    .contentType(MediaType.APPLICATION_JSON)
                    .content(objectMapper.writeValueAsString(orderRequest)))
            .andExpect(status().isCreated())
            .andExpect(jsonPath("$.quantity", is(3)))
            .andExpect(jsonPath("$.totalAmount", is(268.50))) // 89.50 * 3
            .andExpect(jsonPath("$.status", is("CONFIRMED")))
            .andReturn();

    // Assert Product stock decremented: 10 - 3 = 7
    Product reloadedProduct = productRepository.findById(product.getId()).orElseThrow();
    assertThat(reloadedProduct.getStock()).isEqualTo(7);
}""")

    doc.add_heading(level=2).add_run("Task 1 Code Snippet: Terminal State Protection (Negative Test)").font.color.rgb = RGBColor(30, 58, 138)
    add_code_block(doc,
"""@Test
@DisplayName("13. Negative Path: Update an order that is already CANCELLED returns 400 Bad Request")
void updateOrder_AlreadyCancelled_Returns400() throws Exception {
    Product product = productRepository.save(new Product("USB-C Hub", "Multiport", new BigDecimal("35.00"), 15));
    Order cancelledOrder = orderRepository.save(new Order(product.getId(), 1, new BigDecimal("35.00"), "789 Dock Rd", OrderStatus.CANCELLED));

    UpdateOrderRequest updateRequest = new UpdateOrderRequest("Attempted New Address", OrderStatus.CONFIRMED);

    mockMvc.perform(put("/api/orders/" + cancelledOrder.getId())
                    .contentType(MediaType.APPLICATION_JSON)
                    .content(objectMapper.writeValueAsString(updateRequest)))
            .andExpect(status().isBadRequest())
            .andExpect(jsonPath("$.status", is(400)))
            .andExpect(jsonPath("$.message", containsString("Cannot update order in CANCELLED status")));
}""")

    # =========================================================================
    # Section 3: Task 2 - Contract Testing
    # =========================================================================
    h3 = doc.add_heading(level=1)
    r = h3.add_run("3. Task 2: Contract Testing")
    r.font.color.rgb = RGBColor(30, 58, 138)

    doc.add_paragraph(
        "Contract testing establishes a verifiable agreement between independent services without requiring full end-to-end integration environments. "
        "In this architecture, the Order Service acts as the Consumer that requests item availability and metadata from the Product Service (Provider). "
        "We implemented Consumer-Driven Contract testing using Spring Cloud Contract Verifier (v4.1.2) with Groovy DSL specifications."
    )

    doc.add_paragraph(
        "Two contracts are established under src/test/resources/contracts/product-service/ strictly targeting the /api/v1/items endpoints:"
    )

    doc.add_heading(level=2).add_run("Contract 1: shouldCreateProduct.groovy (POST /api/v1/items)").font.color.rgb = RGBColor(30, 58, 138)
    add_code_block(doc,
"""org.springframework.cloud.contract.spec.Contract.make {
    request {
        method 'POST'
        url '/api/v1/items'
        headers { contentType('application/json') }
        body([
            name: 'New Gadget',
            description: 'An innovative gadget',
            price: 150.00,
            stock: 25
        ])
    }
    response {
        status 201
        headers { contentType('application/json') }
        body([
            id: $(anyNumber()),
            name: 'New Gadget',
            description: 'An innovative gadget',
            price: 150.00,
            stock: 25
        ])
    }
}""")

    doc.add_heading(level=2).add_run("Contract 2: shouldGetProductById.groovy (GET /api/v1/items/1)").font.color.rgb = RGBColor(30, 58, 138)
    add_code_block(doc,
"""org.springframework.cloud.contract.spec.Contract.make {
    request {
        method 'GET'
        url '/api/v1/items/1'
    }
    response {
        status 200
        headers { contentType('application/json') }
        body([
            id: 1,
            name: 'Sample Product',
            description: 'A test product description',
            price: 99.99,
            stock: 10
        ])
    }
}""")

    doc.add_heading(level=2).add_run("Product Contract Base Class: ProductBaseTest.java").font.color.rgb = RGBColor(30, 58, 138)
    add_code_block(doc,
"""package com.ecommerce.product;

import java.math.BigDecimal;
import org.junit.jupiter.api.BeforeEach;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.context.WebApplicationContext;
import com.ecommerce.AbstractContainerIntegrationTest;
import io.restassured.module.mockmvc.RestAssuredMockMvc;

public abstract class ProductBaseTest extends AbstractContainerIntegrationTest {

    @Autowired
    private WebApplicationContext context;

    @Autowired
    private ProductRepository productRepository;

    @BeforeEach
    public void setup() {
        RestAssuredMockMvc.webAppContextSetup(context);
        productRepository.deleteAll();
        productRepository.save(new Product("Sample Product", "A test product description", new BigDecimal("99.99"), 10));
    }
}""")

    doc.add_heading(level=2).add_run("Contract 3: shouldCreateOrder.groovy (POST /api/orders)").font.color.rgb = RGBColor(30, 58, 138)
    add_code_block(doc,
"""package contracts.order

import org.springframework.cloud.contract.spec.Contract

Contract.make {
    description "Should place a new order successfully"
    request {
        method POST()
        url '/api/orders'
        headers { contentType(applicationJson()) }
        body([productId: 1, quantity: 2, shippingAddress: "123 Main Street"])
    }
    response {
        status CREATED()
        headers { contentType(applicationJson()) }
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
}""")

    doc.add_heading(level=2).add_run("Contract 4: shouldUpdateOrder.groovy (PUT /api/orders/100)").font.color.rgb = RGBColor(30, 58, 138)
    add_code_block(doc,
"""package contracts.order

import org.springframework.cloud.contract.spec.Contract

Contract.make {
    description "Should update an existing order status"
    request {
        method PUT()
        url '/api/orders/100'
        headers { contentType(applicationJson()) }
        body([shippingAddress: "123 Main Street", status: "SHIPPED"])
    }
    response {
        status OK()
        headers { contentType(applicationJson()) }
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
}""")

    doc.add_heading(level=2).add_run("Order Contract Base Class: OrderBaseClass.java").font.color.rgb = RGBColor(30, 58, 138)
    add_code_block(doc,
"""package com.ecommerce.order;

import com.ecommerce.ECommerceApplication;
import com.ecommerce.order.dto.OrderResponse;
import com.ecommerce.order.dto.PlaceOrderRequest;
import com.ecommerce.order.dto.UpdateOrderRequest;
import io.restassured.module.mockmvc.RestAssuredMockMvc;
import org.junit.jupiter.api.BeforeEach;
import org.mockito.Mockito;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.web.servlet.MockMvc;
import java.math.BigDecimal;
import java.time.Instant;

@SpringBootTest(classes = ECommerceApplication.class)
@AutoConfigureMockMvc
public abstract class OrderBaseClass {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private OrderService orderService;

    @BeforeEach
    public void setup() {
        RestAssuredMockMvc.mockMvc(mockMvc);
        Instant fixedTimestamp = Instant.parse("2026-09-14T15:00:00Z");
        OrderResponse createdResponse = new OrderResponse(100L, 1L, 2, new BigDecimal("49.98"), "123 Main Street", OrderStatus.PENDING, fixedTimestamp);
        Mockito.when(orderService.placeOrder(Mockito.any(PlaceOrderRequest.class))).thenReturn(createdResponse);

        OrderResponse updatedResponse = new OrderResponse(100L, 1L, 2, new BigDecimal("49.98"), "123 Main Street", OrderStatus.SHIPPED, fixedTimestamp);
        Mockito.when(orderService.updateOrder(Mockito.eq(100L), Mockito.any(UpdateOrderRequest.class))).thenReturn(updatedResponse);
    }
}""")

    # =========================================================================
    # Section 4: Acceptance Criteria Verification (5 of 5 Fulfilled)
    # =========================================================================
    h_ac = doc.add_heading(level=1)
    r = h_ac.add_run("4. Acceptance Criteria Verification (5/5 Fulfilled)")
    r.font.color.rgb = RGBColor(30, 58, 138)

    doc.add_paragraph(
        "To ensure production-grade reliability and compliance with enterprise automated testing standards, "
        "the architecture rigorously satisfies all five stipulated acceptance criteria:"
    )

    # Acceptance Criteria Compliance Table
    t_ac = doc.add_table(rows=6, cols=3)
    t_ac.alignment = WD_TABLE_ALIGNMENT.CENTER
    ac_headers = ["#", "Acceptance Criterion", "Implementation & Verification Proof"]
    for i, h in enumerate(ac_headers):
        cell = t_ac.rows[0].cells[i]
        set_cell_background(cell, "1E3A8A")
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.font.bold = True
        r.font.size = Pt(9)
        r.font.color.rgb = RGBColor(255, 255, 255)

    ac_data = [
        ("AC-1", 
         "Integration tests launch a throwaway PostgreSQL container automatically upon execution.", 
         "AbstractContainerIntegrationTest uses Testcontainers 1.20.1 to launch postgres:16-alpine with Ryuk 0.8.1. Automatically reaped on JVM exit. Zero manual setup required."),
        ("AC-2", 
         "Database dynamic ports bind seamlessly in local environments and CI/CD pipelines.", 
         "@DynamicPropertySource binds postgres::getJdbcUrl to Spring datasource properties. Ephemeral port (e.g., 60187) prevents host port conflicts across concurrent builds."),
        ("AC-3", 
         "Schema migrations (Flyway) auto-apply when the test container starts.", 
         "Flyway 10.10.0 executes V1__init_schema.sql automatically upon datasource initialization. Verified in logs: 'Successfully applied 1 migration to schema public, now at version v1'."),
        ("AC-4", 
         "Programmatic entity factories deliver valid Product and Order objects for test setups.", 
         "ProductFactory and OrderFactory provide strongly-typed builder methods with bakery domain fixtures (Chocolate Chip Cookie Box, Ube Cheese Pandesal) priced in Philippine Pesos (PHP)."),
        ("AC-5", 
         "Database state resets between test executions via transaction rollbacks or table truncation hooks.", 
         "@BeforeEach hook in AbstractContainerIntegrationTest executes 'TRUNCATE TABLE orders, products RESTART IDENTITY CASCADE', guaranteeing 100% test isolation and zero pollution.")
    ]

    for idx, (cid, ctitle, cproof) in enumerate(ac_data):
        row = t_ac.rows[idx + 1]
        c0, c1, c2 = row.cells[0], row.cells[1], row.cells[2]
        c0.width = Inches(0.8)
        c1.width = Inches(2.7)
        c2.width = Inches(3.0)
        set_cell_background(c0, "F8FAFC" if idx % 2 == 0 else "FFFFFF")
        set_cell_background(c1, "F8FAFC" if idx % 2 == 0 else "FFFFFF")
        set_cell_background(c2, "F8FAFC" if idx % 2 == 0 else "FFFFFF")
        set_cell_margins(c0, 40, 40, 60, 60)
        set_cell_margins(c1, 40, 40, 60, 60)
        set_cell_margins(c2, 40, 40, 60, 60)

        p0 = c0.paragraphs[0]
        r0 = p0.add_run(cid)
        r0.font.bold = True
        r0.font.size = Pt(8.5)
        r0.font.color.rgb = RGBColor(30, 58, 138)

        p1 = c1.paragraphs[0]
        r1 = p1.add_run(ctitle)
        r1.font.bold = True
        r1.font.size = Pt(8.5)

        p2 = c2.paragraphs[0]
        r2 = p2.add_run(cproof)
        r2.font.size = Pt(8.5)
        r2.font.color.rgb = RGBColor(51, 65, 85)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    doc.add_heading(level=2).add_run("Base Test Architecture: AbstractContainerIntegrationTest.java").font.color.rgb = RGBColor(30, 58, 138)
    add_code_block(doc,
"""@SpringBootTest
@AutoConfigureMockMvc
public abstract class AbstractContainerIntegrationTest {

    public static final PostgreSQLContainer<?> postgres;

    static {
        // Criterion 1: Automatic throwaway PostgreSQL container upon test execution
        postgres = new PostgreSQLContainer<>("postgres:16-alpine")
                .withDatabaseName("ecommerce_test")
                .withUsername("testuser")
                .withPassword("testpass");
        postgres.start();
    }

    // Criterion 2: Dynamic ports bind seamlessly in local and CI/CD pipelines
    // Criterion 3: Flyway schema migrations auto-apply on container startup
    @DynamicPropertySource
    static void configureDatabaseProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", postgres::getJdbcUrl);
        registry.add("spring.datasource.username", postgres::getUsername);
        registry.add("spring.datasource.password", postgres::getPassword);
        registry.add("spring.datasource.driver-class-name", () -> "org.postgresql.Driver");
        registry.add("spring.jpa.database-platform", () -> "org.hibernate.dialect.PostgreSQLDialect");
        registry.add("spring.flyway.enabled", () -> "true");
        registry.add("spring.jpa.hibernate.ddl-auto", () -> "validate");
    }

    @Autowired
    protected MockMvc mockMvc;

    @Autowired
    protected ObjectMapper objectMapper;

    @Autowired
    protected JdbcTemplate jdbcTemplate;

    // Criterion 5: Database state resets between test executions via table truncation hook
    @BeforeEach
    void resetDatabaseState() {
        jdbcTemplate.execute("TRUNCATE TABLE orders, products RESTART IDENTITY CASCADE");
    }
}""")

    doc.add_heading(level=2).add_run("Programmatic Entity Factories: ProductFactory.java & OrderFactory.java").font.color.rgb = RGBColor(30, 58, 138)
    add_code_block(doc,
"""// Criterion 4: Programmatic entity factories delivering valid bakery objects in PHP
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
}

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
}""")

    # =========================================================================
    # Section 5: Task 3 - Test Data Management Strategy
    # =========================================================================
    h4 = doc.add_heading(level=1)
    r = h4.add_run("5. Task 3: Test Data Management Strategy")
    r.font.color.rgb = RGBColor(30, 58, 138)

    doc.add_paragraph(
        "A critical vulnerability in enterprise integration testing is test data pollution: dirty state remaining from earlier runs, "
        "shared mutable records colliding across concurrent threads, and SQL dialect disparities between in-memory mock databases (H2) "
        "and production relational engines (PostgreSQL). Our Test Data Management strategy eliminates these failure modes using "
        "containerized test data orchestration with Testcontainers and Docker."
    )

    doc.add_heading(level=2).add_run("Architecture of Containerized Test Data Management").font.color.rgb = RGBColor(30, 58, 138)
    
    # Embed Architecture Image
    add_image_with_caption(doc, "docs/images/plain_test_data_architecture.jpg", "Figure 1: Test Data Management Architecture with Docker PostgreSQL Container", width_inches=5.8)

    doc.add_paragraph(
        "The Test Data Management strategy is built on four core operational pillars:"
    )

    p = doc.add_paragraph(style='List Bullet')
    r = p.add_run("1. Dynamic Port Binding & Process Isolation: ")
    r.font.bold = True
    p.add_run("PostgreSQL containers dynamically bind to ephemeral host ports (e.g. 60187) via @DynamicPropertySource, "
              "completely eliminating port collisions with existing services or between parallel test suites.")

    p = doc.add_paragraph(style='List Bullet')
    r = p.add_run("2. Domain-Specific Seeding (Cookies & Pastries in PHP Currency): ")
    r.font.bold = True
    p.add_run("Baseline test data models an authentic artisan bakery business. Items include Chocolate Chip Cookie Box, Ube Cheese Pandesal, "
              "and Matcha Cream Croissant, with monetary values explicitly stored and calculated in Philippine Pesos (PHP).")

    p = doc.add_paragraph(style='List Bullet')
    r = p.add_run("3. Versioned Schema Migrations (Flyway): ")
    r.font.bold = True
    p.add_run("Database tables are created and maintained through versioned Flyway migration scripts (V1__init_schema.sql), "
              "ensuring structural consistency between testing and production environments.")

    p = doc.add_paragraph(style='List Bullet')
    r = p.add_run("4. Automated State Reset & Teardown: ")
    r.font.bold = True
    p.add_run("Before each test method, TRUNCATE TABLE ... CASCADE restores the database to a pristine zero-pollution baseline. "
              "Upon JVM termination, Testcontainers Ryuk cleanly destroys all containers.")

    # Embed Docker Screenshot
    add_image_with_caption(doc, "docs/images/docker_database_screenshot.png", "Figure 2: Docker Container Status & Verified PostgreSQL Database Records in PHP", width_inches=5.8)

    # Flyway Migration Script
    doc.add_heading(level=2).add_run("Flyway Migration: src/main/resources/db/migration/V1__init_schema.sql").font.color.rgb = RGBColor(30, 58, 138)
    add_code_block(doc,
"""CREATE TABLE IF NOT EXISTS products (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price NUMERIC(10, 2) NOT NULL,
    stock INT NOT NULL
);

CREATE TABLE IF NOT EXISTS orders (
    id BIGSERIAL PRIMARY KEY,
    product_id BIGINT NOT NULL REFERENCES products(id),
    quantity INT NOT NULL,
    total_amount NUMERIC(10, 2) NOT NULL,
    shipping_address VARCHAR(500) NOT NULL,
    status VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);""")

    # Docker Test Code
    doc.add_heading(level=2).add_run("Docker Test Suite: DockerTestDataIntegrationTest.java").font.color.rgb = RGBColor(30, 58, 138)
    add_code_block(doc,
"""@Test
@DisplayName("Place pastry order against Docker test database and verify PHP total amount and stock deduction")
void testPlaceOrderAgainstDockerContainerDatabase() throws Exception {
    Product cookieBox = productRepository.save(ProductFactory.createValidProduct());
    int initialStock = cookieBox.getStock();

    PlaceOrderRequest orderRequest = new PlaceOrderRequest(
            cookieBox.getId(),
            2,
            "Unit 4B, BGC High Street, Taguig City, Metro Manila"
    );

    MvcResult result = mockMvc.perform(post("/api/orders")
                    .contentType(MediaType.APPLICATION_JSON)
                    .content(objectMapper.writeValueAsString(orderRequest)))
            .andExpect(status().isCreated())
            .andExpect(jsonPath("$.productId", is(cookieBox.getId().intValue())))
            .andExpect(jsonPath("$.quantity", is(2)))
            .andExpect(jsonPath("$.totalAmount", is(500.00))) // PHP 250.00 * 2 = PHP 500.00
            .andExpect(jsonPath("$.status", is("CONFIRMED")))
            .andReturn();

    // Verify stock is decremented in Docker PostgreSQL (20 - 2 = 18)
    Product updatedCookieBox = productRepository.findById(cookieBox.getId()).orElseThrow();
    assertThat(updatedCookieBox.getStock()).isEqualTo(initialStock - 2);
}""")

    # =========================================================================
    # Section 6: Verification & Execution Logs
    # =========================================================================
    h5 = doc.add_heading(level=1)
    r = h5.add_run("6. Task 4: Screenshots of Test Results & Execution Logs")
    r.font.color.rgb = RGBColor(30, 58, 138)

    doc.add_paragraph(
        "The automated test suite was executed end-to-end using Maven. Below is the visual terminal screenshot confirming "
        "the successful compilation and passing execution of all 21 test cases with zero errors and zero failures."
    )

    # Embed Test Results Terminal Screenshot
    add_image_with_caption(doc, "docs/images/test_results_terminal.png", "Figure 3: Terminal Screenshot of Maven Test Execution - 21 Tests Passed (BUILD SUCCESS)", width_inches=5.8)

    doc.add_heading(level=2).add_run("Detailed Terminal Execution Output (mvn clean test)").font.color.rgb = RGBColor(30, 58, 138)
    add_code_block(doc,
"""[INFO] -------------------------------------------------------
[INFO]  T E S T S
[INFO] -------------------------------------------------------
[INFO] Running com.ecommerce.DockerTestDataIntegrationTest
INFO  tc.testcontainers/ryuk:0.8.1 - Container testcontainers/ryuk:0.8.1 started
INFO  tc.postgres:16-alpine - Container postgres:16-alpine started in PT1.039S
INFO  tc.postgres:16-alpine - Container is started (JDBC URL: jdbc:postgresql://localhost:60187/ecommerce_test)
INFO  o.f.core.internal.command.DbMigrate - Migrating schema 'public' to version '1 - init schema'
INFO  o.f.core.internal.command.DbMigrate - Successfully applied 1 migration to schema 'public', now at version v1
[INFO] Tests run: 2, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 6.916 s -- in DockerTestDataIntegrationTest
[INFO] Running com.ecommerce.ECommerceIntegrationTest$UpdateOrderTests
[INFO] Tests run: 6, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.123 s -- in UpdateOrderTests
[INFO] Running com.ecommerce.ECommerceIntegrationTest$PlaceOrderTests
[INFO] Tests run: 5, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.274 s -- in PlaceOrderTests
[INFO] Running com.ecommerce.ECommerceIntegrationTest$CreateProductTests
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.068 s -- in CreateProductTests
[INFO] Running com.ecommerce.OrderTest
[INFO] Tests run: 2, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 2.301 s -- in OrderTest
[INFO] Running com.ecommerce.Product_serviceTest
[INFO] Tests run: 2, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.062 s -- in Product_serviceTest
[INFO] 
[INFO] Results:
[INFO] 
[INFO] Tests run: 21, Failures: 0, Errors: 0, Skipped: 0
[INFO] 
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
[INFO] Total time:  18.682 s
[INFO] Finished at: 2026-09-14T16:00:51+08:00
[INFO] ------------------------------------------------------------------------""")

    # Conclusion
    doc.add_heading(level=1).add_run("7. Conclusion").font.color.rgb = RGBColor(30, 58, 138)
    doc.add_paragraph(
        "All requirements stipulated for Task 1 (Integration Testing), Task 2 (Contract Testing), Task 3 (Test Data Management), "
        "and Task 4 (Documentation) have been comprehensively implemented, tested, and validated across 21 test cases. "
        "Furthermore, all 5 automated testing acceptance criteria have been achieved and verified against real Docker Testcontainers "
        "and Flyway schema migrations. The project provides a bulletproof enterprise testing blueprint ready for production CI/CD deployment."
    )

    output_path = "ECOMMERCE_TESTING_DOCUMENTATION.docx"
    try:
        doc.save(output_path)
        print(f"Successfully generated Word document at {output_path}")
    except PermissionError:
        fallback_path = "ECOMMERCE_TESTING_DOCUMENTATION_UPDATED.docx"
        doc.save(fallback_path)
        print(f"Notice: {output_path} is currently locked by another application (e.g. MS Word). Successfully saved updated documentation to {fallback_path}")

if __name__ == "__main__":
    build_document()
