-- create-category_tab
-- depends:

-- migrate: apply
CREATE TABLE IF NOT EXISTS category_tab (
    category_id BIGSERIAL NOT NULL PRIMARY KEY,
    name VARCHAR(150) NOT NULL UNIQUE,
    description VARCHAR(255),
    parent_id BIGINT
);

-- migrate: rollback
DROP TABLE category_tab CASCADE;
