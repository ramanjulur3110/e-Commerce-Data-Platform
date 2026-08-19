# E-Commerce Simulator — Deployment Guide

This guide covers deploying the e-commerce simulator from a fresh environment using Docker Compose.

The application consists of three primary containers:

* **PostgreSQL** — persistent OLTP database
* **Order Generator** — continuously generates simulated e-commerce transactions
* **Payment Processor** — independently processes payments and advances transaction states

The application services use dedicated PostgreSQL service accounts rather than the database administrator account.

---

## Prerequisites

The deployment machine requires:

* Docker
* Docker Compose
* Git, if cloning directly from the repository

Verify Docker is available:

```bash
docker --version
docker compose version
```

---

## 1. Clone or Copy the Project

Clone the repository:

```bash
git clone <repository-url>
cd <repository-directory>
```

Alternatively, copy the project directory to the target machine.

The project should contain the Docker Compose file, application Dockerfiles, source code, and database initialization scripts.

Example:

```text
project/
├── src/
├── ddl_scripts/
│   ├── generator_schema.sql
│   ├── static_data.sql
│   └── service_accounts.sql
├── Dockerfile.generator
├── Dockerfile.payment-processor
├── docker-compose.yml
├── .env
└── ...
```

The `.env` file should **not** be committed to Git.

---

## 2. Create the Environment File

Create a `.env` file in the same directory as `docker-compose.yml`.

Example:

```env
POSTGRES_DB=mydatabase

ORDER_GENERATOR_DB_USER=order_generator_svc
ORDER_GENERATOR_DB_PASSWORD=<generator-password>

PAYMENT_PROCESSOR_DB_USER=payment_processor_svc
PAYMENT_PROCESSOR_DB_PASSWORD=<processor-password>
```

Use your own passwords.

The service-account passwords in this file **must match the passwords assigned to the corresponding PostgreSQL roles** during database initialization.

Make sure `.env` is included in `.gitignore`:

```gitignore
.env
```

---

## 3. Build the Containers

Build and create the containers without starting the application:

```bash
docker compose up --build --no-start
```

This prepares PostgreSQL, the order generator, and the payment processor.

---

## 4. Start PostgreSQL

Start only the database:

```bash
docker compose start db
```

Verify that PostgreSQL started successfully:

```bash
docker logs generator_postgres
```

Wait until PostgreSQL reports that it is ready to accept connections before continuing.

---

## 5. Create the Database Schema

Load the current database definition:

```bash
docker exec -i generator_postgres \
  psql -U admin -d mydatabase \
  < ddl_scripts/generator_schema.sql
```

This creates the `generator` schema and its required tables, sequences, constraints, and other database objects.

---

## 6. Load Static Data

Load the reference and seed data:

```bash
docker exec -i generator_postgres \
  psql -U admin -d mydatabase \
  < ddl_scripts/static_data.sql
```

Static data includes tables such as:

```text
customers
product_categories
product_subcategories
products
payment_type
ref_shipping_rates
ref_tax_rates
```

Transactional tables intentionally begin empty.

The order generator and payment processor will populate those tables once the services start.

---

## 7. Create the Service Accounts

The application uses separate PostgreSQL accounts for its runtime services.

Create:

```sql
CREATE USER order_generator_svc
WITH PASSWORD '<same password as ORDER_GENERATOR_DB_PASSWORD>';

CREATE USER payment_processor_svc
WITH PASSWORD '<same password as PAYMENT_PROCESSOR_DB_PASSWORD>';
```

These commands can be executed through `psql`:

```bash
docker exec -it generator_postgres \
  psql -U admin -d mydatabase
```

Then execute the SQL and exit with:

```text
\q
```

**Important:** The passwords must match the corresponding values in `.env`.

---

## 8. Apply Service Permissions

Apply the service-account grants:

```bash
docker exec -i generator_postgres \
  psql -U admin -d mydatabase \
  < ddl_scripts/service_accounts.sql
```

The service accounts follow a least-privilege model.

### Order Generator

`order_generator_svc` has the permissions required to:

* Read static/reference data
* Create orders
* Create order details
* Create payment records
* Create initial payment history
* Create order status history

### Payment Processor

`payment_processor_svc` has the permissions required to:

* Read and update payment records
* Update applicable order states
* Insert/update payment status history
* Insert/update order status history

Neither application service should require PostgreSQL administrator credentials during normal operation.

---

## 9. Start the Application Services

Once the database, static data, roles, and permissions are ready:

```bash
docker compose start generator payment-processor
```

Alternatively:

```bash
docker compose up -d
```

---

## 10. Verify the Services

Check the order generator:

```bash
docker logs -f order_generator_app
```

Check the payment processor:

```bash
docker logs -f payment_processor_app
```

Use `Ctrl+C` to stop following the logs. This does **not** stop the container.

Verify container status:

```bash
docker compose ps
```

All three services should be running.

---

## 11. Verify Database Activity

Connect to PostgreSQL:

```bash
docker exec -it generator_postgres \
  psql -U admin -d mydatabase
```

Check generated orders:

```sql
SELECT COUNT(*)
FROM generator.orders;
```

Check payment states:

```sql
SELECT payment_status, COUNT(*)
FROM generator.payment_orders
GROUP BY payment_status
ORDER BY payment_status;
```

Check order states:

```sql
SELECT order_status, COUNT(*)
FROM generator.orders
GROUP BY order_status
ORDER BY order_status;
```

Exit PostgreSQL:

```text
\q
```

---

## Service Architecture

```text
                  ┌──────────────────────┐
                  │     PostgreSQL       │
                  │     mydatabase       │
                  │                      │
                  │  generator schema    │
                  └──────────┬───────────┘
                             │
              ┌──────────────┴──────────────┐
              │                             │
              │                             │
┌─────────────▼─────────────┐   ┌──────────▼──────────────┐
│     Order Generator       │   │    Payment Processor    │
│                           │   │                         │
│ order_generator_svc       │   │ payment_processor_svc   │
│                           │   │                         │
│ Generates transactions    │   │ Processes payments      │
└───────────────────────────┘   └─────────────────────────┘
```

PostgreSQL administrator credentials are intended for deployment, schema management, and maintenance.

Runtime application processes use dedicated service accounts.

---

## Stopping the Application

Stop the containers without deleting them:

```bash
docker compose stop
```

Start them again:

```bash
docker compose start
```

---

## Rebuilding Application Containers

After changing application code:

```bash
docker compose up --build -d
```

This rebuilds the application images while retaining the PostgreSQL volume.

---

## Complete Environment Reset

**Warning: The following command deletes the PostgreSQL Docker volume and all generated database data.**

```bash
docker compose down -v
```

Afterward, repeat the deployment process:

```text
Build containers
      ↓
Start PostgreSQL
      ↓
Load generator_schema.sql
      ↓
Load static_data.sql
      ↓
Create service accounts
      ↓
Apply service-account grants
      ↓
Start application services
```

Do not use `docker compose down -v` unless destroying the existing database is intentional.

---

## Local Development

The application can also be executed directly through Python without Docker.

Local development can use a PostgreSQL development/admin account through environment variables such as:

```env
DB_HOST=localhost
DB_PORT=5433
DB_NAME=mydatabase
DB_USER=admin
DB_PASSWORD=admin
```

Example generator execution:

```bash
uv run python -u -m src.generator.bootstrap_generator
```

The Docker deployment overrides these generic `DB_*` variables with the appropriate service-account credentials.

Therefore, the Python application code does not need separate database connection logic for local and containerized execution.

---

## Deployment Model

The project intentionally separates deployment privileges from runtime privileges:

```text
Deployment / Database Administration
              │
            admin
              │
      ┌───────┴────────┐
      │ Schema / Roles │
      │ Static Data    │
      │ Permissions    │
      └───────┬────────┘
              │
        Runtime Services
              │
       ┌──────┴───────┐
       │              │
order_generator_svc   payment_processor_svc
       │              │
 Order Generator    Payment Processor
```

This allows the database to be initialized and maintained with elevated privileges while keeping continuously running application processes restricted to only the permissions they require.
