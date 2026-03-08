# Database Service

PostgreSQL database for e-commerce application data persistence.

## Schema

### Tables

#### products
- `id` - Primary key
- `name` - Product name
- `description` - Product description
- `price` - Product price (DECIMAL)
- `stock` - Available stock quantity
- `active` - Active status flag
- `created_at` - Creation timestamp
- `updated_at` - Last update timestamp

#### orders
- `id` - Primary key
- `customer_email` - Customer email address
- `total_amount` - Order total (DECIMAL)
- `status` - Order status (pending, processing, shipped, delivered, cancelled)
- `created_at` - Creation timestamp
- `updated_at` - Last update timestamp

#### order_items
- `id` - Primary key
- `order_id` - Foreign key to orders table
- `product_id` - Foreign key to products table
- `quantity` - Quantity ordered
- `price` - Price at time of order
- `created_at` - Creation timestamp

## Setup

### Prerequisites
- PostgreSQL 12+ installed and running
- Python 3.8+ with psycopg2

### Installation

1. Install PostgreSQL (if not already installed):
```bash
# Ubuntu/Debian
sudo apt-get install postgresql postgresql-contrib

# macOS
brew install postgresql
```

2. Start PostgreSQL service:
```bash
# Ubuntu/Debian
sudo service postgresql start

# macOS
brew services start postgresql
```

3. Install Python dependencies:
```bash
pip install psycopg2-binary
```

### Initialize Database

Run the setup script:
```bash
python setup.py
```

Or manually using psql:
```bash
psql -U postgres -f schema.sql
```

## Configuration

### Environment Variables
- `DB_HOST` - Database host (default: localhost)
- `DB_PORT` - Database port (default: 5432)
- `DB_NAME` - Database name (default: ecommerce)
- `DB_USER` - Database user (default: postgres)
- `DB_PASSWORD` - Database password (default: postgres)

### Connection String
```
postgresql://postgres:postgres@localhost:5432/ecommerce
```

## Sample Data

The schema includes sample product data:
- Laptop ($999.99)
- Smartphone ($699.99)
- Headphones ($199.99)
- Tablet ($499.99)
- Smartwatch ($299.99)

## Maintenance

### Backup
```bash
pg_dump -U postgres ecommerce > backup.sql
```

### Restore
```bash
psql -U postgres ecommerce < backup.sql
```

### Reset Database
```bash
psql -U postgres -c "DROP DATABASE ecommerce;"
python setup.py
```
