-- ===================================================================
-- SCRIPT 01: ZOMATO RESTAURANT TABLE SCHEMA
-- Compatible with MySQL, PostgreSQL, and SQLite
-- ===================================================================

DROP TABLE IF EXISTS restaurants;

CREATE TABLE restaurants (
    restaurant_id VARCHAR(30) PRIMARY KEY,
    restaurant_name VARCHAR(150),
    city VARCHAR(50),
    locality VARCHAR(100),
    cuisine VARCHAR(50),
    average_cost_for_two INT,
    price_category VARCHAR(50),
    has_online_delivery VARCHAR(5),
    has_table_booking VARCHAR(5),
    rating DECIMAL(3, 1),
    rating_status VARCHAR(30),
    votes INT,
    delivery_time_min INT
);

-- Indexing for fast analytical querying
CREATE INDEX idx_city ON restaurants(city);
CREATE INDEX idx_cuisine ON restaurants(cuisine);
CREATE INDEX idx_rating ON restaurants(rating);
