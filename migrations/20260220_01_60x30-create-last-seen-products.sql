-- create last seen products
-- depends: 20260127_01_igbxa-create-category-table

-- migrate: apply
CREATE TABLE IF NOT EXISTS last_seen_products (
    id SERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    product_id BIGINT NOT NULL,
    last_seen_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    -- CONSTRAINT last_seen_products_fk1
    --     FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,

    CONSTRAINT last_seen_products_fk2
        FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,

    CONSTRAINT unique_user_product
        UNIQUE (user_id, product_id)
);

-- migrate: rollback
DROP TABLE last_seen_products RESTART IDENTITY CASCADE;


