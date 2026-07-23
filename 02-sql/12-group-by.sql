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
	) AS "고객당 평균 주문수",
	SUM(total_amount)::FLOAT / COUNT(DISTINCT customer_id) AS 고객당평균매출
FROM sales
GROUP BY region
ORDER BY 고객당평균매출 DESC;


-- 영업사원별 월별 매출
-- 영업사원, 월, 월주문건수, 월총매출액, 월평균매출액
SELECT
	sales_rep AS 영업사원,
	TO_CHAR(order_date, 'YYYY-MM') AS 월,
	COUNT(*) AS 주문건수,
	SUM(total_amount) AS 월총매출액,
	ROUND(AVG(total_amount), 2) AS 월평균매출액
FROM sales
GROUP BY 
	sales_rep,
	TO_CHAR(order_date, 'YYYY-MM')
ORDER BY sales_rep, 월;

-- MAU (Monthly Active User) -> 월간활성고객
-- 월별로, [월, 주문건수, 매출액, MAU]  (해당 월에 주문한 사용자 수)
SELECT
	TO_CHAR(order_date, 'YYYY-MM') AS 월,
	COUNT(*) AS 주문건수,
	SUM(total_amount) AS 매출액,
	COUNT(DISTINCT customer_id) AS MAU
FROM sales
GROUP BY TO_CHAR(order_date, 'YYYY-MM')
ORDER BY 월;

-- 요일별 매출 패턴
SELECT
	EXTRACT(DOW FROM order_date) AS 요일번호,
	TO_CHAR(order_date, 'Day') AS 요일,
	COUNT(*) AS 주문건수,
	SUM(total_amount) AS 매출액,
	ROUND(AVG(total_amount), 2) AS 평균매출액
FROM sales
GROUP BY
	EXTRACT(DOW FROM order_date), -- 요일번호
	TO_CHAR(order_date, 'Day') -- 요일
ORDER BY 매출액 DESC;
