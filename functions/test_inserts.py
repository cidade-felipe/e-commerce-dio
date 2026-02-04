import random
import string
import time
import uuid

import psycopg as psy

from conect_db import connect_to_db


NAMES = ["Ana", "Bruno", "Carla", "Diego", "Erica", "Fabio", "Gabi", "Hugo", "Iara", "Joao"]
LAST_NAMES = ["Silva", "Souza", "Pereira", "Lima", "Gomes", "Ribeiro", "Almeida", "Costa", "Rocha", "Mendes"]
CITIES = ["Sao Paulo", "Rio de Janeiro", "Curitiba", "Recife", "Salvador", "Porto Alegre", "Campinas"]
STATES = ["SP", "RJ", "PR", "PE", "BA", "RS"]
PRODUCT_ADJ = ["Basico", "Premium", "Leve", "Esportivo", "Classico", "Compacto"]
PRODUCT_NOUN = ["Camiseta", "Relogio", "Mochila", "Tenis", "Fone", "Garrafa"]
CATEGORY_DESC = ["Roupas casuais", "Acessorios", "Tecnologia", "Esportes", "Casa e Jardim"]
ORDER_DESC = ["Compra online", "Compra express", "Compra promocional", "Compra em lote"]
SUPPLIER_NAMES = ["Fornecedor Alpha", "Fornecedor Beta", "Fornecedor Gamma", "Fornecedor Delta"]
SELLER_NAMES = ["Vendedor Centro", "Vendedor Sul", "Vendedor Norte", "Vendedor Leste"]


def rand_digits(n):
    return "".join(random.choice(string.digits) for _ in range(n))


def rand_email():
    return f"user_{uuid.uuid4().hex[:10]}@example.com"


def rand_phone():
    return f"{random.randint(10, 99)}9{rand_digits(8)}"


def rand_address():
    return f"Rua {random.choice(string.ascii_uppercase)}, {random.randint(10, 999)}"


def rand_product_name():
    return f"{random.choice(PRODUCT_NOUN)} {random.choice(PRODUCT_ADJ)}"


def rand_tracking_code(state):
    return f"BR{rand_digits(9)}{state}"


def rand_company_suffix():
    return random.choice(["LTDA", "SA", "ME", "EIRELI"])


def insert_data():
    conn_info = connect_to_db()
    with psy.connect(conn_info) as conn:
        with conn.cursor() as cur:
            # Clients
            cur.execute(
                """
                INSERT INTO client (email, phone, address, city, state)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (email) DO UPDATE SET
                    phone = EXCLUDED.phone,
                    address = EXCLUDED.address,
                    city = EXCLUDED.city,
                    state = EXCLUDED.state
                RETURNING id
                """,
                (
                    rand_email(),
                    rand_phone(),
                    rand_address(),
                    random.choice(CITIES),
                    random.choice(STATES),
                ),
            )
            client1_id = cur.fetchone()[0]

            cur.execute(
                """
                INSERT INTO client (email, phone, address, city, state)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (email) DO UPDATE SET
                    phone = EXCLUDED.phone,
                    address = EXCLUDED.address,
                    city = EXCLUDED.city,
                    state = EXCLUDED.state
                RETURNING id
                """,
                (
                    rand_email(),
                    rand_phone(),
                    rand_address(),
                    random.choice(CITIES),
                    random.choice(STATES),
                ),
            )
            client2_id = cur.fetchone()[0]

            # Customers
            cur.execute(
                """
                INSERT INTO individual_customer (client_id, fname, mname, lname, cpf)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (cpf) DO UPDATE SET
                    client_id = EXCLUDED.client_id,
                    fname = EXCLUDED.fname,
                    mname = EXCLUDED.mname,
                    lname = EXCLUDED.lname
                RETURNING id
                """,
                (
                    client1_id,
                    random.choice(NAMES),
                    random.choice(string.ascii_uppercase),
                    random.choice(LAST_NAMES),
                    rand_digits(11),
                ),
            )
            individual_id = cur.fetchone()[0]

            cur.execute(
                """
                INSERT INTO corporate_customer (client_id, corporate_name, cnpj)
                VALUES (%s, %s, %s)
                ON CONFLICT (cnpj) DO UPDATE SET
                    client_id = EXCLUDED.client_id,
                    corporate_name = EXCLUDED.corporate_name
                RETURNING id
                """,
                (
                    client2_id,
                    f"{random.choice(SELLER_NAMES)} {rand_company_suffix()}",
                    rand_digits(14),
                ),
            )
            corporate_id = cur.fetchone()[0]

            # Categories
            cur.execute(
                """
                INSERT INTO category (review_score, size, description)
                VALUES (%s, %s, %s)
                RETURNING id
                """,
                (round(random.uniform(3.0, 5.0), 2), random.choice(["P", "M", "G", "U"]), random.choice(CATEGORY_DESC)),
            )
            category1_id = cur.fetchone()[0]

            cur.execute(
                """
                INSERT INTO category (review_score, size, description)
                VALUES (%s, %s, %s)
                RETURNING id
                """,
                (round(random.uniform(3.0, 5.0), 2), random.choice(["P", "M", "G", "U"]), random.choice(CATEGORY_DESC)),
            )
            category2_id = cur.fetchone()[0]

            # Products
            cur.execute(
                """
                INSERT INTO product (client_id, category_id, name, price, classification_kids)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
                """,
                (
                    client1_id,
                    category1_id,
                    rand_product_name(),
                    round(random.uniform(20.0, 500.0), 2),
                    random.choice([True, False]),
                ),
            )
            product1_id = cur.fetchone()[0]

            cur.execute(
                """
                INSERT INTO product (client_id, category_id, name, price, classification_kids)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
                """,
                (
                    client2_id,
                    category2_id,
                    rand_product_name(),
                    round(random.uniform(20.0, 500.0), 2),
                    random.choice([True, False]),
                ),
            )
            product2_id = cur.fetchone()[0]

            # Stock
            cur.execute(
                """
                INSERT INTO stock (place)
                VALUES (%s)
                RETURNING id
                """,
                (f"CD {random.choice(CITIES)}",),
            )
            stock1_id = cur.fetchone()[0]

            cur.execute(
                """
                INSERT INTO stock (place)
                VALUES (%s)
                RETURNING id
                """,
                (f"CD {random.choice(CITIES)}",),
            )
            stock2_id = cur.fetchone()[0]

            # Product stock
            cur.execute(
                """
                INSERT INTO product_stock (product_id, stock_id, quantity)
                VALUES (%s, %s, %s)
                """,
                (product1_id, stock1_id, random.randint(10, 200)),
            )
            cur.execute(
                """
                INSERT INTO product_stock (product_id, stock_id, quantity)
                VALUES (%s, %s, %s)
                """,
                (product2_id, stock2_id, random.randint(10, 200)),
            )

            # Orders
            cur.execute(
                """
                INSERT INTO "order" (order_status, order_description, send_value, client_id, product_id)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
                """,
                (
                    random.choice(["DELIVERED", "PENDING", "CANCELLED"]),
                    random.choice(ORDER_DESC),
                    round(random.uniform(5.0, 50.0), 2),
                    client1_id,
                    product1_id,
                ),
            )
            order1_id = cur.fetchone()[0]

            cur.execute(
                """
                INSERT INTO "order" (order_status, order_description, send_value, client_id, product_id)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
                """,
                (
                    random.choice(["DELIVERED", "PENDING", "CANCELLED"]),
                    random.choice(ORDER_DESC),
                    round(random.uniform(5.0, 50.0), 2),
                    client2_id,
                    product2_id,
                ),
            )
            order2_id = cur.fetchone()[0]

            # Suppliers
            cur.execute(
                """
                INSERT INTO supplier (social_name, cnpj, contact)
                VALUES (%s, %s, %s)
                ON CONFLICT (cnpj) DO UPDATE SET
                    social_name = EXCLUDED.social_name,
                    contact = EXCLUDED.contact
                RETURNING id
                """,
                (
                    random.choice(SUPPLIER_NAMES),
                    rand_digits(14),
                    f"contato{rand_digits(4)}@supplier.com",
                ),
            )
            supplier1_id = cur.fetchone()[0]

            cur.execute(
                """
                INSERT INTO supplier (social_name, cnpj, contact)
                VALUES (%s, %s, %s)
                ON CONFLICT (cnpj) DO UPDATE SET
                    social_name = EXCLUDED.social_name,
                    contact = EXCLUDED.contact
                RETURNING id
                """,
                (
                    random.choice(SUPPLIER_NAMES),
                    rand_digits(14),
                    f"contato{rand_digits(4)}@supplier.com",
                ),
            )
            supplier2_id = cur.fetchone()[0]

            # Product supplier
            cur.execute(
                """
                INSERT INTO product_supplier (product_id, supplier_id)
                VALUES (%s, %s)
                """,
                (product1_id, supplier1_id),
            )
            cur.execute(
                """
                INSERT INTO product_supplier (product_id, supplier_id)
                VALUES (%s, %s)
                """,
                (product2_id, supplier2_id),
            )

            # Sellers
            cur.execute(
                """
                INSERT INTO seller (social_name, cnpj, contact, address, city, state)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (cnpj) DO UPDATE SET
                    social_name = EXCLUDED.social_name,
                    contact = EXCLUDED.contact,
                    address = EXCLUDED.address,
                    city = EXCLUDED.city,
                    state = EXCLUDED.state
                RETURNING id
                """,
                (
                    random.choice(SELLER_NAMES),
                    rand_digits(14),
                    f"vendedor{rand_digits(4)}@seller.com",
                    rand_address(),
                    random.choice(CITIES),
                    random.choice(STATES),
                ),
            )
            seller1_id = cur.fetchone()[0]

            cur.execute(
                """
                INSERT INTO seller (social_name, cnpj, contact, address, city, state)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (cnpj) DO UPDATE SET
                    social_name = EXCLUDED.social_name,
                    contact = EXCLUDED.contact,
                    address = EXCLUDED.address,
                    city = EXCLUDED.city,
                    state = EXCLUDED.state
                RETURNING id
                """,
                (
                    random.choice(SELLER_NAMES),
                    rand_digits(14),
                    f"vendedor{rand_digits(4)}@seller.com",
                    rand_address(),
                    random.choice(CITIES),
                    random.choice(STATES),
                ),
            )
            seller2_id = cur.fetchone()[0]

            # Product seller
            cur.execute(
                """
                INSERT INTO product_seller (product_id, seller_id)
                VALUES (%s, %s)
                """,
                (product1_id, seller1_id),
            )
            cur.execute(
                """
                INSERT INTO product_seller (product_id, seller_id)
                VALUES (%s, %s)
                """,
                (product2_id, seller2_id),
            )

            # Payments
            cur.execute(
                """
                INSERT INTO payment (payment_type, order_id)
                VALUES (%s, %s)
                """,
                (random.choice(["CASH", "DEBIT", "CREDIT", "PIX"]), order1_id),
            )
            cur.execute(
                """
                INSERT INTO payment (payment_type, order_id)
                VALUES (%s, %s)
                """,
                (random.choice(["CASH", "DEBIT", "CREDIT", "PIX"]), order2_id),
            )

            # Product order
            cur.execute(
                """
                INSERT INTO product_order (product_id, order_id, quantity)
                VALUES (%s, %s, %s)
                """,
                (product1_id, order1_id, random.randint(1, 10)),
            )
            cur.execute(
                """
                INSERT INTO product_order (product_id, order_id, quantity)
                VALUES (%s, %s, %s)
                """,
                (product2_id, order2_id, random.randint(1, 10)),
            )

            # Delivery
            order1_state = random.choice(STATES)
            order2_state = random.choice(STATES)
            cur.execute(
                """
                INSERT INTO delivery (order_id, status, tracking_code)
                VALUES (%s, %s, %s)
                """,
                (order1_id, random.choice(["DELIVERED", "PENDING", "CANCELLED"]), rand_tracking_code(order1_state)),
            )
            cur.execute(
                """
                INSERT INTO delivery (order_id, status, tracking_code)
                VALUES (%s, %s, %s)
                """,
                (order2_id, random.choice(["DELIVERED", "PENDING", "CANCELLED"]), rand_tracking_code(order2_state)),
            )

    run_id = uuid.uuid4().hex[:8]
    print(
        f"Dados de teste inseridos com sucesso (run={run_id}):",
        f"clients=({client1_id}, {client2_id})",
        f"individual_customer={individual_id}",
        f"corporate_customer={corporate_id}",
        f"products=({product1_id}, {product2_id})",
        f"orders=({order1_id}, {order2_id})",
    )


if __name__ == "__main__":
    random.seed(time.time_ns())
    insert_data()
