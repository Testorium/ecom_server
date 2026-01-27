-- create products table
-- depends:

-- migrate: apply
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    price NUMERIC(10, 2) NOT NULL CHECK (price >= 0),
    quantity INT NOT NULL CHECK (quantity >= 0),
    description VARCHAR(255)
);

-- migrate: rollback
DROP TABLE products RESTART IDENTITY CASCADE;
