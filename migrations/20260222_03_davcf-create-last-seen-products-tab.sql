-- create-last_seen_products_tab
-- depends: 20260222_02_tyrq6-create-product-tab

-- migrate: apply
CREATE TABLE IF NOT EXISTS last_seen_product_tab (
    last_seen_product_id SERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    product_id BIGINT NOT NULL,
    last_seen_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    -- CONSTRAINT last_seen_products_tab_fk1
    --     FOREIGN KEY (user_id) REFERENCES user_tab(user_tab) ON DELETE CASCADE,

    CONSTRAINT last_seen_products_tab_fk2
        FOREIGN KEY (product_id) REFERENCES product_tab(product_id) ON DELETE CASCADE,

    CONSTRAINT unique_user_product
        UNIQUE (user_id, product_id)
);

-- migrate: rollback
DROP TABLE last_seen_product_tab CASCADE;


