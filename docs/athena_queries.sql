-- Count offers by category
SELECT category, COUNT(*) AS total_offers
FROM job_offer_db.job_offers
GROUP BY category
ORDER BY total_offers DESC;

-- Count offers by level
SELECT level, COUNT(*) AS total_offers
FROM job_offer_db.job_offers
GROUP BY level
ORDER BY total_offers DESC;

-- Count offers by category and level
SELECT category, level, COUNT(*) AS total_offers
FROM job_offer_db.job_offers
GROUP BY category, level
ORDER BY category, level;

-- Sample records
SELECT text, category, level
FROM job_offer_db.job_offers
LIMIT 10;

-- Text length analysis
SELECT
    category,
    AVG(LENGTH(text)) AS avg_text_length,
    MIN(LENGTH(text)) AS min_text_length,
    MAX(LENGTH(text)) AS max_text_length
FROM job_offer_db.job_offers
GROUP BY category
ORDER BY avg_text_length DESC;