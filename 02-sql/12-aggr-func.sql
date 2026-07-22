-- 12-aggr-func.sql
-- id,order_date,customer_id,product_id,product_name,category,quantity,unit_price,total_amount,sales_rep,region

SELECT * FROM sales;

-- COUNT
SELECT
	COUNT(*) AS 총주문건수,
	COUNT(DISTINCT customer_id) AS 고객수,
	COUNT(DISTINCT product_name) AS 상품종류수
FROM sales;

-- SUM
SELECT
	SUM(total_amount) AS 총매출액,
	TO_CHAR(SUM(total_amount), 'FM999,999,999') || '원' AS 읽기쉽게,
	SUM(quantity) AS 총판매수량
FROM sales;

-- region '서울' 발생한 총 매출액과 주문건수
SELECT
	SUM(total_amount) AS 서울매출총액,
	COUNT(*) AS 서울주문건수
FROM sales
WHERE region = '서울';

-- AVG
SELECT
	AVG(total_amount) AS 회당평균주문액,
	AVG(quantity) AS 평균구매수량,
	ROUND(AVG(unit_price), 2) AS 평균단가  -- ROUND(x, 3) -> x를 소숫점 3자리 반올림
FROM sales;

-- MIN MAX
SELECT
	MIN(total_amount) AS 최소매출액,
	MAX(total_amount) AS 최대매출액,
	MIN(order_date) AS 첫주문일,
	MAX(order_date) AS 마지막주문일
FROM sales;

-- 매출 대시보드
SELECT
	COUNT(*) AS 주문건수,
	SUM(total_amount) AS 총매출액,
	ROUND(AVG(total_amount), 1) AS 평균매출액,  -- 소숫점 1자리까지
	MAX(total_amount) AS 최대매출액,
	ROUND(AVG(quantity), 3) AS 평균구매수량 -- 소숫점 3자리
FROM sales
WHERE region='광주';


























