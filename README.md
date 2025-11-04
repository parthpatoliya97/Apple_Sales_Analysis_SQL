## SQL Project - Apple Sales Analysis

![apple_store](https://static0.makeuseofimages.com/wordpress/wp-content/uploads/2023/04/apple-store-with-apple-logo-in-the-background.jpg)

## ER Diagram :-
![ER Diagram](<img width="1284" height="426" alt="image" src="https://github.com/user-attachments/assets/eb38eb99-8aac-4ecf-913b-f3bcb89f24f7" />
)

#### 1.Find the number of stores in each country
```sql
SELECT 
    country, 
    COUNT(store_id) AS total_stores
FROM store
GROUP BY country;
```

#### 2.Total number of units sold by each store
```sql
SELECT 
    s.store_id,
    st.store_name,
    SUM(s.quantity) AS total_units
FROM store st
JOIN sales s ON st.store_id = s.store_id
GROUP BY s.store_id, st.store_name;
```

#### 3.Number of sales in December 2023
```sql
SELECT
    COUNT(*) AS sales_in_december
FROM sales
WHERE DATE_FORMAT(sale_date, '%m-%Y') = '12-2023';
```

#### 4.Stores with no warranty claim filed

#### Method 1: Using HAVING
```sql
SELECT 
    st.store_id,
    st.store_name,
    COUNT(w.claim_id) AS total_claims
FROM store st
LEFT JOIN sales s ON st.store_id = s.store_id
LEFT JOIN warranty w ON s.sale_id = w.sale_id
GROUP BY st.store_id, st.store_name
HAVING COUNT(w.claim_id) = 0;
```

#### Method 2: Using NOT IN
```sql
SELECT 
    st.store_id,
    st.store_name
FROM store st
WHERE st.store_id NOT IN (
    SELECT DISTINCT s.store_id
    FROM sales s
    JOIN warranty w ON s.sale_id = w.sale_id
);
```

#### 5.Percentage of "Warranty Void" claims
```sql
SELECT 
    COUNT(*) AS total_claims,
    COUNT(CASE WHEN repair_status = 'Warranty Void' THEN 1 END) AS void_claims,
    ROUND(COUNT(CASE WHEN repair_status = 'Warranty Void' THEN 1 END) * 100.0 / COUNT(*), 2) AS void_percentage
FROM warranty;
```

#### 6.Store with highest total units sold (2022)
```sql
SELECT 
    st.store_id,
    st.store_name,
    SUM(s.quantity) AS total_units
FROM store st
JOIN sales s ON st.store_id = s.store_id
WHERE YEAR(s.sale_date) = '2022'
GROUP BY st.store_id, st.store_name
ORDER BY total_units DESC;
```

#### 7.Unique products sold in 2022
```sql
SELECT COUNT(DISTINCT product_id) AS unique_products_sold
FROM sales 
WHERE YEAR(sale_date) = '2022';
```

#### 8.Average product price by category
#### Simple Average :-
```sql
SELECT 
    c.category_name,
    ROUND(AVG(p.price), 2) AS avg_price
FROM products p
JOIN category c ON p.category_id = c.category_id
GROUP BY c.category_name;
```

#### Detailed Stats :-
```sql
SELECT 
    c.category_name,
    COUNT(p.product_id) AS product_count,
    ROUND(MIN(p.price), 2) AS min_price,
    ROUND(MAX(p.price), 2) AS max_price,
    ROUND(AVG(p.price), 2) AS avg_price,
    ROUND(STDDEV(p.price), 2) AS price_std_dev
FROM products p
JOIN category c ON p.category_id = c.category_id
GROUP BY c.category_name
ORDER BY avg_price DESC;
```

#### 9.Warranty claims in 2022
```sql
SELECT COUNT(*) AS total_claims
FROM warranty
WHERE YEAR(claim_date) = '2022';
```

#### 10.Best-selling day for each store
```sql
WITH cte AS (
    SELECT 
        store_id,
        DAYNAME(sale_date) AS day_name,
        SUM(quantity) AS total_quantity,
        DENSE_RANK() OVER(PARTITION BY store_id ORDER BY SUM(quantity) DESC) AS rnk
    FROM sales
    GROUP BY store_id, DAYNAME(sale_date)
)
SELECT store_id, day_name, total_quantity
FROM cte 
WHERE rnk = 1;
```

#### 11.Least selling product per country (year-wise)
```sql
WITH cte AS (
    SELECT 
        YEAR(s.sale_date) AS year_,
        st.country,
        p.product_name,
        SUM(s.quantity) AS total_sold,
        DENSE_RANK() OVER (
            PARTITION BY YEAR(s.sale_date), st.country 
            ORDER BY SUM(s.quantity)
        ) AS rnk
    FROM sales s
    JOIN store st ON s.store_id = st.store_id
    JOIN products p ON s.product_id = p.product_id
    GROUP BY YEAR(s.sale_date), st.country, p.product_name
)
SELECT 
    year_,
    country,
    product_name,
    total_sold
FROM cte
WHERE rnk = 1
ORDER BY year_, country, total_sold;
```

#### 12.Warranty claims filed within 180 days of sale
```sql
SELECT COUNT(*) AS claims_within_180_days
FROM sales s
JOIN warranty w ON s.sale_id = w.sale_id
WHERE DATEDIFF(w.claim_date, s.sale_date) <= 180;
```

#### 13.Warranty claims for products launched in last 2 years
```sql
SELECT 
    p.product_id,
    p.product_name,
    p.launch_date,
    COUNT(w.claim_id) AS total_claims
FROM products p
JOIN sales s ON p.product_id = s.product_id
JOIN warranty w ON s.sale_id = w.sale_id
WHERE YEAR(p.launch_date) IN (2022, 2023)
GROUP BY p.product_id, p.product_name, p.launch_date
ORDER BY total_claims DESC;
```

#### 14.Months (last 3 years) with sales > 5000 units (USA)
```sql
SELECT 
    YEAR(s.sale_date) AS year_,
    MONTH(s.sale_date) AS month_,
    MONTHNAME(s.sale_date) AS month_name,
    SUM(s.quantity) AS total_units
FROM store st
JOIN sales s ON st.store_id = s.store_id
WHERE st.country = 'USA'
    AND s.sale_date >= DATE_SUB(CURDATE(), INTERVAL 3 YEAR)
GROUP BY YEAR(s.sale_date), MONTH(s.sale_date), MONTHNAME(s.sale_date)
HAVING SUM(s.quantity) > 5000
ORDER BY year_, month_;
```

#### 15.Product category with most warranty claims (last 2 years)
```sql
SELECT 
    c.category_name,
    COUNT(w.claim_id) AS total_claims
FROM sales s
JOIN warranty w ON s.sale_id = w.sale_id
JOIN products p ON s.product_id = p.product_id
JOIN category c ON p.category_id = c.category_id
WHERE YEAR(w.claim_date) IN (2022, 2023)
GROUP BY c.category_name
ORDER BY total_claims DESC;
```

#### 16.Warranty claim percentage per country
```sql
WITH cte AS (
    SELECT 
        st.country,
        SUM(s.quantity) AS total_purchase,
        COUNT(w.claim_id) AS total_claims
    FROM sales s
    JOIN store st ON s.store_id = st.store_id
    LEFT JOIN warranty w ON s.sale_id = w.sale_id
    GROUP BY st.country
)
SELECT 
    country,
    total_purchase,
    total_claims,
    ROUND((total_claims / total_purchase) * 100, 2) AS claim_percent
FROM cte;
```

#### 17.Yearly growth ratio per store
```sql
WITH cte AS (
    SELECT 
        st.store_id,
        st.store_name,
        st.city,
        YEAR(s.sale_date) AS year_,
        SUM(s.quantity) AS current_sale,
        LAG(SUM(s.quantity), 1) OVER(PARTITION BY st.store_id ORDER BY YEAR(s.sale_date)) AS previous_sale
    FROM store st
    JOIN sales s ON st.store_id = s.store_id
    GROUP BY st.store_id, st.store_name, st.city, YEAR(s.sale_date)
)
SELECT 
    store_id,
    store_name,
    city,
    year_,
    ROUND(((current_sale - previous_sale) / previous_sale) * 100, 2) AS growth_ratio
FROM cte;
```

#### 18.Correlation between product price & warranty claims
```sql
SELECT 
    p.product_name,
    p.price,
    COUNT(w.claim_id) AS total_claims
FROM sales s
JOIN products p ON s.product_id = p.product_id
JOIN warranty w ON s.sale_id = w.sale_id
WHERE s.sale_date >= CURDATE() - INTERVAL 5 YEAR
GROUP BY p.product_name, p.price;
```

#### 19.Store with highest % of "Paid Repaired" claims
```sql
WITH cte AS (
    SELECT 
        st.store_id,
        st.store_name,
        COUNT(w.claim_id) AS total_claims,
        SUM(CASE WHEN w.repair_status = 'Paid Repaired' THEN 1 ELSE 0 END) AS paid_claims
    FROM sales s
    JOIN store st ON s.store_id = st.store_id
    JOIN warranty w ON s.sale_id = w.sale_id
    GROUP BY st.store_id, st.store_name
)
SELECT 
    store_id,
    store_name,
    total_claims,
    paid_claims,
    ROUND((paid_claims / total_claims) * 100, 2) AS paid_claim_percent
FROM cte
ORDER BY paid_claim_percent DESC;
```

#### 20.Monthly running total of sales per store
```sql
WITH cte AS (
    SELECT 
        st.store_id,
        st.store_name,
        MONTH(s.sale_date) AS month_,
        YEAR(s.sale_date) AS year_,
        SUM(s.quantity) AS total_sales
    FROM sales s
    JOIN store st ON s.store_id = st.store_id
    GROUP BY st.store_id, st.store_name, MONTH(s.sale_date), YEAR(s.sale_date)
)
SELECT 
    store_id,
    store_name,
    year_,
    month_,
    total_sales,
    SUM(total_sales) OVER(PARTITION BY store_id ORDER BY year_, month_) AS running_total
FROM cte;
```

#### 21.Product sales trends based on launch period
```sql
SELECT 
    p.product_id,
    p.product_name,
    CASE 
        WHEN s.sale_date BETWEEN p.launch_date AND p.launch_date + INTERVAL 6 MONTH THEN '0-6 months'
        WHEN s.sale_date BETWEEN p.launch_date + INTERVAL 6 MONTH AND p.launch_date + INTERVAL 12 MONTH THEN '6-12 months'
        WHEN s.sale_date BETWEEN p.launch_date + INTERVAL 12 MONTH AND p.launch_date + INTERVAL 18 MONTH THEN '12-18 months'
        ELSE '18+ months'
    END AS period,
    SUM(s.quantity) AS total_units_sold
FROM sales s
JOIN products p ON s.product_id = p.product_id
GROUP BY p.product_id, p.product_name, period
ORDER BY p.product_id, period;
```
