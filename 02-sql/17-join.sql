-- 17-join.sql

SELECT * FROM sales;
SELECT * FROM customers;

-- JOIN 좌우 결합
-- INNER JOIN 왼쪽테이블과 오른쪽 테이블 모두 만족하는 교집합 데이터만 -> 구매와 고객 모두 만족
SELECT 
	*
FROM sales s  -- 테이블명 줄여서 말하기
INNER JOIN customers c ON s.customer_id=c.customer_id

-- LEFT JOIN 왼쪽의 모든 데이터 + (있을경우) 오른쪽의 매칭되는 데이터 -> 구매 안한 고객도 나옴
SELECT 
	*
FROM customers c
LEFT JOIN sales s ON s.customer_id=c.customer_id

-- VIP 고객들(c)의 구매내역(s)을 조회
SELECT 
	*
FROM customers c
INNER JOIN sales s ON c.customer_id=s.customer_id
WHERE c.customer_type='VIP' AND total_amount >= POWER(10, 6);

-- 각 등급(c)별 구매액(s) 평균 확인
SELECT 
	c.customer_type AS 등급,
	COUNT(*) AS 구매수,
	COUNT(DISTINCT s.customer_id) AS 고객수,
	ROUND(AVG(s.total_amount), 2) AS 평균구매액
FROM customers c
INNER JOIN sales s ON c.customer_id=s.customer_id
GROUP BY c.customer_type;

-- 모든 고객의 고객별 구매 현황 분석
-- 고객이름, 등급, 주문횟수,
-- 총 구매액(없으면 0), 평균주문액(없으면 0.0), 최근주문일(없으면 '주문없음')
SELECT
	c.customer_id,
	c.customer_name,
	c.customer_type,
	COUNT(s.id) AS 주문횟수,
	COALESCE(SUM(s.total_amount), 0) AS 총구매액,
	COALESCE(AVG(s.total_amount), 0) AS 평균주문액,
	COALESCE(
		TO_CHAR(MAX(s.order_date), 'YYYY-MM-DD'), '주문없음'
	) AS 최근주문일,
	CASE
        WHEN COUNT(s.id) = 0   THEN '잠재고객'
        WHEN COUNT(s.id) >= 5  THEN '충성고객'
        WHEN COUNT(s.id) >= 2  THEN '일반고객'
        ELSE '신규고객'
    END AS 고객분류
FROM customers c
LEFT JOIN sales s 
ON c.customer_id=s.customer_id 
GROUP BY c.customer_id
ORDER BY c.customer_id;













