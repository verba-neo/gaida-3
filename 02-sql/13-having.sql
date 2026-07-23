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


SELECT
	category,
	COUNT(*) AS 주문건수,
	SUM(total_amount) AS 매출액
FROM sales
GROUP BY category
HAVING SUM(total_amount) >= POWER(10, 7);









