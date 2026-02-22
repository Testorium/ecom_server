-- create-product_tab
-- depends: 20260222_01_l6ish-create-category-tab

-- migrate: apply
CREATE TABLE IF NOT EXISTS product_tab (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    description TEXT,
    summary VARCHAR(255),
    category_id BIGINT NOT NULL,
    is_deleted BOOLEAN DEFAULT FALSE,
    is_archived BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT product_tab_fk1
        FOREIGN KEY (category_id) REFERENCES category_tab(category_id) ON DELETE RESTRICT
);

-- migrate: rollback
DROP TABLE IF EXISTS product_tab CASCADE;

