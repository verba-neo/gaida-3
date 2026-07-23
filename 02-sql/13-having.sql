-- 13-having.sql
/*
SQL 실행 순서
1. FROM
2. WHERE
3. GROUP BY
4. HAVING
5. SELECT   ← 여기서 컬럼 alias가 만들어짐 (AS)
6. ORDER BY
*/

-- 원본 데이터중에 매출 100만원 이상만 가지고 피벗 테이블 만들기
SELECT
	category,
	COUNT(*) AS 주문건수,
	SUM(total_amount) AS 총매출
FROM sales
WHERE total_amount >= 1000000
GROUP BY category;

-- 피벗테이블에서 (카테고리별로) 매출액 10^7 이상만 보기
SELECT
	category,
	COUNT(*) AS 주문건수,
	SUM(total_amount) AS 매출액
FROM sales
GROUP BY category
HAVING SUM(total_amount) >= POWER(10, 7);


-- 활성지역 찾기 -> 지역별
-- 지역, 주문건수, 고객수, 매출액 (고객수 >= 15 and 주문건수 >= 20)
SELECT
	region AS 지역,
	COUNT(*) AS 주문건수,
	COUNT(DISTINCT customer_id) AS 고객수,
	SUM(total_amount) AS 매출액
FROM sales
GROUP BY region
HAVING 
	COUNT(DISTINCT customer_id) >= 15 AND
	COUNT(*) >= 20;


-- 우수영업 사원 -> 달 평균 매출액 130만원 이상인 영업사원
-- 영업사원, 판매건수, 고객수, 총매출, [활동개월수, 월평균매출]
SELECT
	sales_rep,
	COUNT(*) AS 판매건수,
	COUNT(DISTINCT customer_id) AS 고객수,
	SUM(total_amount) AS 총매출,
	COUNT(DISTINCT TO_CHAR(order_date, 'YYYY-MM')) AS 활동개월수,
	SUM(total_amount)::FLOAT / COUNT(DISTINCT TO_CHAR(order_date, 'YYYY-MM')) AS 월평균매출
FROM sales
GROUP BY sales_rep



