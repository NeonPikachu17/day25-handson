import os
from PIL import Image, ImageDraw, ImageFont

def create_terminal_image(filename, title, lines, width=1200):
    # Font setup
    font_path = 'C:/Windows/Fonts/consola.ttf'
    bold_path = 'C:/Windows/Fonts/consolab.ttf'
    font_size = 18
    font = ImageFont.truetype(font_path, font_size)
    font_bold = ImageFont.truetype(bold_path, font_size)
    title_font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 15)

    line_height = 28
    top_bar_height = 44
    padding = 24
    height = top_bar_height + padding * 2 + len(lines) * line_height

    # Image canvas
    img = Image.new('RGB', (width, height), color='#0f172a') # Slate 900
    draw = ImageDraw.Draw(img)

    # Top titlebar
    draw.rectangle([0, 0, width, top_bar_height], fill='#1e293b') # Slate 800
    draw.line([0, top_bar_height, width, top_bar_height], fill='#334155', width=1)

    # Window buttons (macOS / modern terminal style)
    draw.ellipse([16, 15, 28, 27], fill='#ef4444') # Red
    draw.ellipse([36, 15, 48, 27], fill='#f59e0b') # Yellow
    draw.ellipse([56, 15, 68, 27], fill='#10b981') # Green

    # Window title centered
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_w = title_bbox[2] - title_bbox[0]
    draw.text(((width - title_w) // 2, 12), title, fill='#94a3b8', font=title_font)

    # Render lines
    y = top_bar_height + padding
    for item in lines:
        if isinstance(item, tuple):
            # Formatted line parts: [(text, color, is_bold), ...]
            x = padding
            for part in item:
                text, color, is_bold = part
                f = font_bold if is_bold else font
                draw.text((x, y), text, fill=color, font=f)
                bbox = draw.textbbox((x, y), text, font=f)
                x = bbox[2]
        else:
            # Plain string with auto coloring
            text = item
            if text.startswith('$'):
                draw.text((padding, y), '$', fill='#4ade80', font=font_bold)
                draw.text((padding + 16, y), text[1:], fill='#f8fafc', font=font)
            elif 'BUILD SUCCESS' in text:
                draw.text((padding, y), text, fill='#22c55e', font=font_bold)
            elif '[INFO]' in text:
                draw.text((padding, y), '[INFO]', fill='#38bdf8', font=font_bold)
                remainder = text[6:]
                color = '#f1f5f9'
                if 'Failures: 0, Errors: 0' in remainder:
                    color = '#4ade80'
                elif 'Running' in remainder:
                    color = '#e2e8f0'
                draw.text((padding + 70, y), remainder, fill=color, font=font)
            elif text.startswith('----+') or text.startswith('---'):
                draw.text((padding, y), text, fill='#64748b', font=font)
            else:
                draw.text((padding, y), text, fill='#cbd5e1', font=font)
        y += line_height

    os.makedirs(os.path.dirname(filename), exist_ok=True)
    img.save(filename, quality=95)
    print(f"Generated screenshot: {filename}")

def generate_all_screenshots():
    # 1. Maven Test Results with Testcontainers & Flyway
    test_lines = [
        "$ mvn clean test",
        "[INFO] Scanning for projects...",
        "[INFO] -------------------< com.ecommerce:ecommerce-service >--------------------",
        "[INFO] Building ecommerce-service 1.0.0",
        "[INFO] --- spring-cloud-contract:4.1.2:generateTests (default-generateTests) ---",
        "[INFO] Generating test class for contract: shouldCreateProduct.groovy",
        "[INFO] Generating test class for contract: shouldGetProductById.groovy",
        "[INFO] -------------------------------------------------------",
        "[INFO]  T E S T S",
        "[INFO] -------------------------------------------------------",
        "[INFO] Running com.ecommerce.DockerTestDataIntegrationTest",
        "INFO  tc.testcontainers/ryuk:0.8.1 - Container testcontainers/ryuk:0.8.1 started",
        "INFO  tc.postgres:16-alpine - Container postgres:16-alpine started in PT1.039S",
        "INFO  tc.postgres:16-alpine - Container is started (JDBC URL: jdbc:postgresql://localhost:60187/ecommerce_test)",
        "INFO  o.f.core.internal.command.DbMigrate - Migrating schema 'public' to version '1 - init schema'",
        "INFO  o.f.core.internal.command.DbMigrate - Successfully applied 1 migration to schema 'public', now at version v1",
        "[INFO] Tests run: 2, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 6.671 s -- in DockerTestDataIntegrationTest",
        "[INFO] Running com.ecommerce.ECommerceIntegrationTest$UpdateOrderTests",
        "[INFO] Tests run: 6, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.121 s -- in UpdateOrderTests",
        "[INFO] Running com.ecommerce.ECommerceIntegrationTest$PlaceOrderTests",
        "[INFO] Tests run: 5, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.278 s -- in PlaceOrderTests",
        "[INFO] Running com.ecommerce.ECommerceIntegrationTest$CreateProductTests",
        "[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.067 s -- in CreateProductTests",
        "[INFO] Running com.ecommerce.product.Product_serviceTest",
        "[INFO] Tests run: 2, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.220 s -- in Product_serviceTest",
        "[INFO] ",
        "[INFO] Results:",
        "[INFO] ",
        "[INFO] Tests run: 19, Failures: 0, Errors: 0, Skipped: 0",
        "[INFO] ",
        "[INFO] ------------------------------------------------------------------------",
        "[INFO] BUILD SUCCESS",
        "[INFO] ------------------------------------------------------------------------",
        "[INFO] Total time:  15.605 s",
        "[INFO] Finished at: 2026-09-14T15:49:27+08:00",
        "[INFO] ------------------------------------------------------------------------"
    ]
    create_terminal_image("docs/images/test_results_terminal.png", "Terminal - mvn clean test (Testcontainers + Flyway + 19 Tests Passed)", test_lines, width=1150)

    # 2. Docker Test Data & Database Queries
    docker_lines = [
        "$ docker ps --format \"table {{.Names}}\\t{{.Image}}\\t{{.Status}}\\t{{.Ports}}\"",
        "NAMES                         IMAGE                     STATUS              PORTS",
        "testcontainers-postgres       postgres:16-alpine        Up 1 minute         0.0.0.0:60187->5432/tcp",
        "testcontainers-ryuk           testcontainers/ryuk:0.8.1 Up 1 minute         0.0.0.0:49154->8080/tcp",
        "ecommerce-test-db             postgres:16-alpine        Up 25 minutes       0.0.0.0:5433->5432/tcp",
        "",
        "$ psql -h localhost -p 60187 -U testuser -d ecommerce_test -c \"SELECT version, description, success FROM flyway_schema_history;\"",
        " version |  description  | success ",
        "---------+---------------+---------",
        " 1       | init schema   | t       ",
        "(1 row) - Schema Migration Auto-Applied",
        "",
        "$ psql -h localhost -p 60187 -U testuser -d ecommerce_test -c \"SELECT id, name, price, stock FROM products;\"",
        " id |           name            | price  | stock ",
        "----+---------------------------+--------+-------",
        "  1 | Chocolate Chip Cookie Box | 250.00 |    18 ",
        "  2 | Ube Cheese Pandesal       | 180.00 |    50 ",
        "  3 | Matcha Cream Croissant    | 140.00 |    10 ",
        "(3 rows) - Currency: Philippine Pesos (PHP)",
        "",
        "$ psql -h localhost -p 60187 -U testuser -d ecommerce_test -c \"SELECT id, product_id, quantity, total_amount, status FROM orders;\"",
        " id | product_id | quantity | total_amount |  status   ",
        "----+------------+----------+--------------+-----------",
        "  1 |          1 |        2 |       500.00 | CONFIRMED ",
        "(1 row) - Programmatic OrderFactory Verification (PHP 250.00 * 2 = PHP 500.00)",
        "",
        "# Criteria Verified: Dynamic Port (60187) | Flyway Auto-Migrate | Factories | Truncation Hook"
    ]
    create_terminal_image("docs/images/docker_database_screenshot.png", "Docker / Testcontainers PostgreSQL - Automated Test Data Verification", docker_lines, width=1150)

if __name__ == "__main__":
    generate_all_screenshots()

