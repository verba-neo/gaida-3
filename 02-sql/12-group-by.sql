-- 12-group-by.sql

SELECT * FROM sales;

-- 지역별로 건당 주문액이 가장 많은 순서로 지역/건수/매출/주문액 확인
SELECT
	region AS 지역,
	COUNT(*) AS 주문건수,
	SUM(total_amount) AS 총매출,
	SUM(total_amount) / COUNT(*) AS 건당주문액
FROM sales
GROUP BY region
ORDER BY 건당주문액 DESC
LIMIT 5;


-- 영업사원 별 - 지역 별 ...
SELECT
	sales_rep AS 영업사원,
	region AS 지역,
	SUM(total_amount) AS 총매출,
	ROUND(AVG(total_amount), 2) AS 평균매출
FROM sales
GROUP BY sales_rep, region
ORDER BY 영업사원, 평균매출 DESC;

-- 지역별 매출 분석
-- 지역, 주문건수, 총매출, [고객수(DISTINCT), 고객당평균주문수, 고객당평균매출]
SELECT
	region AS 지역,
	COUNT(*) AS 주문건수,
	SUM(total_amount) AS 총매출,
	COUNT(DISTINCT customer_id) AS 고객수,
	-- 정수/정수 -> 정수 | 실수 / 정수 -> 실수. 둘중 하나만 실수로 바꾸면 된다.
	ROUND(
		COUNT(*)::DECIMAL / COUNT(DISTINCT customer_id), 2
	) AS 고객당평균주문수,
	SUM(total_amount)::FLOAT / COUNT(DISTINCT customer_id) AS 고객당평균매출
FROM sales
GROUP BY region
ORDER BY 고객당평균매출 DESC;







