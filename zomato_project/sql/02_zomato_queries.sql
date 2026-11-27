-- ===================================================================
-- SCRIPT 02: 5 ESSENTIAL ANALYTICAL SQL QUERIES (ZOMATO)
-- These show real-world SQL skills: Aggregations, GROUP BY, CASE WHEN, CTE
-- ===================================================================

-- -------------------------------------------------------------
-- QUERY 1: Most Popular Cuisines & Their Average Customer Ratings
-- Business Question: What food do people love most, and which gets the best ratings?
-- -------------------------------------------------------------
SELECT 
    cuisine,
    COUNT(restaurant_id) AS total_restaurants,
    ROUND(COUNT(restaurant_id) * 100.0 / (SELECT COUNT(*) FROM restaurants), 2) AS market_share_pct,
    ROUND(AVG(average_cost_for_two), 0) AS avg_cost_for_two_inr,
    ROUND(AVG(rating), 2) AS avg_customer_rating,
    SUM(votes) AS total_customer_votes
FROM restaurants
GROUP BY cuisine
ORDER BY total_restaurants DESC;


-- -------------------------------------------------------------
-- QUERY 2: Online Delivery vs Dine-In Performance
-- Business Question: Do restaurants offering online delivery get more votes and better engagement?
-- -------------------------------------------------------------
SELECT 
    has_online_delivery,
    COUNT(restaurant_id) AS total_restaurants,
    ROUND(AVG(rating), 2) AS avg_rating,
    ROUND(AVG(average_cost_for_two), 0) AS avg_cost_for_two_inr,
    ROUND(AVG(votes), 0) AS avg_votes_per_restaurant
FROM restaurants
GROUP BY has_online_delivery;


-- -------------------------------------------------------------
-- QUERY 3: Delivery Time Impact on Customer Ratings (The Latency Penalty)
-- Business Question: At what delivery time do customers start giving poor reviews?
-- -------------------------------------------------------------
SELECT 
    CASE 
        WHEN delivery_time_min <= 30 THEN '1. Fast (< 30 mins)'
        WHEN delivery_time_min BETWEEN 31 AND 45 THEN '2. Standard (31 - 45 mins)'
        ELSE '3. Delayed (> 45 mins)'
    END AS delivery_speed_tier,
    COUNT(restaurant_id) AS restaurant_count,
    ROUND(AVG(rating), 2) AS avg_customer_rating,
    SUM(CASE WHEN rating < 3.5 THEN 1 ELSE 0 END) AS low_rated_count,
    ROUND(SUM(CASE WHEN rating < 3.5 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS low_rating_pct
FROM restaurants
WHERE has_online_delivery = 'Yes'
GROUP BY 1
ORDER BY 1;


-- -------------------------------------------------------------
-- QUERY 4: City-wise Food Economics & Restaurant Density
-- Business Question: Which cities have the most restaurants and where is dining out most expensive?
-- -------------------------------------------------------------
SELECT 
    city,
    COUNT(restaurant_id) AS total_restaurants,
    ROUND(AVG(average_cost_for_two), 0) AS avg_cost_for_two_inr,
    ROUND(AVG(rating), 2) AS avg_city_rating,
    ROUND(SUM(CASE WHEN has_online_delivery = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS online_delivery_available_pct
FROM restaurants
GROUP BY city
ORDER BY total_restaurants DESC;


-- -------------------------------------------------------------
-- QUERY 5: Top 10 High-Demand Localities (Most Voted Dining Hubs)
-- Business Question: Where are the biggest food clusters in major cities?
-- -------------------------------------------------------------
SELECT 
    city,
    locality,
    COUNT(restaurant_id) AS restaurant_count,
    SUM(votes) AS total_votes_received,
    ROUND(AVG(rating), 2) AS avg_rating,
    ROUND(AVG(average_cost_for_two), 0) AS avg_cost_inr
FROM restaurants
GROUP BY city, locality
ORDER BY total_votes_received DESC
LIMIT 10;
