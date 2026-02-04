-- create products table
-- depends:

-- migrate: apply
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    description TEXT,
    summary VARCHAR(255),
    category_id BIGINT NOT NULL,
    is_deleted BOOLEAN DEFAULT FALSE,
    is_archived BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- migrate: rollback
DROP TABLE products RESTART IDENTITY CASCADE;
