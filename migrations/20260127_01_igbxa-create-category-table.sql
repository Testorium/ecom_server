-- create category table
-- depends: 20260126_01_pc9rr-create-products-table

-- migrate: apply
CREATE TABLE IF NOT EXISTS categories (
    id BIGSERIAL NOT NULL PRIMARY KEY,
    name VARCHAR(150) NOT NULL UNIQUE,
    description VARCHAR(255),
    parent_id BIGINT
);

-- migrate: rollback
DROP TABLE categories RESTART IDENTITY CASCADE;
