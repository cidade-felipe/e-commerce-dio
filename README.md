# E-commerce DIO (PostgreSQL + Python)

Projeto de estudo para o curso **Formação SQL Database Specialist** da [DIO.me](https://web.dio.me/), com modelagem de um e-commerce em PostgreSQL e scripts em Python para criação, remoção e popularização das tabelas.

**Stack**

- PostgreSQL
- Python (psycopg, python-dotenv)

**Estrutura**

- `sql/tables.sql`: definição das tabelas e relacionamentos.
- `functions/conect_db.py`: leitura de `.env` e montagem da string de conexão.
- `functions/create_tables.py`: cria as tabelas do arquivo SQL.
- `functions/drop_tables.py`: remove tabelas do schema informado.
- `functions/test_inserts.py`: insere dados de teste.

**Pré-requisitos**

- PostgreSQL em execução
- Python 3.x

**Configuração**

- Crie um arquivo `.env` com as variáveis abaixo (baseado em `.env_exemple`).
- Ajuste usuário, senha e host conforme seu ambiente.

```env
DB_NAME=e-commerce-dio
DB_USER=postgres
DB_PASSWORD=sua_senha_aqui
DB_HOST=localhost
DB_PORT=5432
DB_POOL_URL=postgresql+psycopg2://postgres:sua_senha_aqui@localhost:5432/e-commerce-dio
```

**Instalação de dependências**

```bash
python -m pip install psycopg[binary] python-dotenv
```

**Como usar**

1. Criar as tabelas:

```bash
python functions/create_tables.py
```

2. Inserir dados de teste (randômicos a cada execução):

```bash
python functions/test_inserts.py
```

3. Remover tabelas do schema:

```bash
python functions/drop_tables.py
```

**Schema (tabelas principais)**

- `client`
- `individual_customer`
- `corporate_customer`
- `category`
- `product`
- `stock`
- `product_stock`
- `"order"` (usa aspas por ser palavra reservada)
- `seller_supplier`
- `product_seller_supplier`
- `payment`
- `product_order`
- `delivery`

**Diagrama ER (Mermaid)**

`ORDER` representa a tabela `"order"`.

```mermaid
erDiagram
  CLIENT {
    int id PK
    varchar email
    varchar phone
    varchar address
    varchar city
    varchar state
  }

  INDIVIDUAL_CUSTOMER {
    int id PK
    int client_id FK
    varchar fname
    varchar mname
    varchar lname
    varchar cpf
  }

  CORPORATE_CUSTOMER {
    int id PK
    int client_id FK
    varchar corporate_name
    varchar cnpj
  }

  CATEGORY {
    int id PK
    numeric review_score
    varchar size
    text description
  }

  PRODUCT {
    int id PK
    int client_id FK
    int category_id FK
    varchar name
    decimal price
    boolean classification_kids
  }

  STOCK {
    int id PK
    varchar place
  }

  PRODUCT_STOCK {
    int id PK
    int product_id FK
    int stock_id FK
    int quantity
  }

  ORDER {
    int id PK
    varchar order_status
    text order_description
    decimal send_value
    int client_id FK
    int product_id FK
  }

  SELLER_SUPPLIER {
    int id PK
    varchar social_name
    varchar cnpj
    varchar contact
    varchar email
    varchar type
    varchar address
    varchar city
    varchar state
  }

  PRODUCT_SELLER_SUPPLIER {
    int id PK
    int product_id FK
    int seller_supplier_id FK
  }

  PAYMENT {
    int id PK
    varchar payment_type
    int order_id FK
  }

  PRODUCT_ORDER {
    int id PK
    int product_id FK
    int order_id FK
    int quantity
  }

  DELIVERY {
    int id PK
    int order_id FK
    varchar status
    varchar tracking_code
  }

  CLIENT ||--o{ INDIVIDUAL_CUSTOMER : has
  CLIENT ||--o{ CORPORATE_CUSTOMER : has
  CLIENT ||--o{ PRODUCT : lists
  CATEGORY ||--o{ PRODUCT : groups
  PRODUCT ||--o{ PRODUCT_STOCK : stocked_in
  STOCK ||--o{ PRODUCT_STOCK : stores
  CLIENT ||--o{ ORDER : places
  PRODUCT ||--o{ ORDER : includes
  PRODUCT ||--o{ PRODUCT_ORDER : item
  ORDER ||--o{ PRODUCT_ORDER : contains
  SELLER_SUPPLIER ||--o{ PRODUCT_SELLER_SUPPLIER : provides
  PRODUCT ||--o{ PRODUCT_SELLER_SUPPLIER : supplied_by
  ORDER ||--o{ PAYMENT : paid_by
  ORDER ||--o{ DELIVERY : ships
  
```

**Queries (notebooks/queries.ipynb)**
`query1`

```sql
SELECT 
  c.id as "ID Cliente",
  po.quantity as "Quantidade",
  o.id as "ID do pedido"
  from client c
  join "order" o on c.id = o.client_id
  join product_order po on po.order_id = o.id
  order by c.id;
```

`query2`

```sql
SELECT
      ss.social_name AS "Razão Social",
      ss.type
      FROM seller_supplier ss
      GROUP BY ss.social_name, ss.type
      HAVING type = 'BOTH';
```

`query3`

```sql
SELECT
      p.id AS "ID do produto",
      p.name AS "Nome do produto",
      p.price AS "Preço"
      FROM product p
      WHERE p.price > 100
      ORDER BY p.price DESC;
```

`query4`

```sql
SELECT
      p.name AS "Nome do Produto",
      p.price AS "Preço do Produto",
      ss.social_name AS "Razão Social",
      pss.seller_supplier_id,
      pss.product_id
      FROM product_seller_supplier pss
      JOIN product p ON p.id = pss.product_id
      JOIN seller_supplier ss ON ss.id = pss.seller_supplier_id
      WHERE ss.type IN ('SUPPLIER', 'BOTH')
      GROUP BY p.name,p.price, ss.social_name, pss.seller_supplier_id, pss.product_id
      ORDER BY p.name, ss.social_name;
```

**Observações**

- A tabela `"order"` é palavra reservada em SQL; por isso é criada e referenciada com aspas.
- As relações de chave estrangeira exigem a criação das tabelas na ordem correta (já contemplada no `tables.sql`).

**Problemas comuns**

- `psycopg.errors.UndefinedTable`: verifique se `category` foi criada antes de `product`.
- `relation "order" does not exist`: garanta o uso de `"order"` com aspas nas consultas.
