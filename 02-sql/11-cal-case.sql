-- 11-cal-case.sql
SELECT * FROM dt_demo;

SELECT
	name,
	score AS 원점수,
	ROUND(score) AS 반올림,
	CEIL(score) AS 올림,
	FLOOR(score) AS 내림
FROM dt_demo;

SELECT
	10 + 5 AS plus,
	10 - 5 AS minus,
	10 * 5 AS multiply,
	10 / 5 AS divide,
	10 / 3 AS 몫,
	10 % 3 AS 나머지,
	POWER(10, 3) AS 거듭제곱,
	SQRT(9) AS 루트,
	ABS(-5) AS 절댓값;

-- CASE
SELECT 
	name,
	score,
	CASE
		WHEN score >= 90 THEN 'A'
		WHEN score >= 80 THEN 'B'
		WHEN score >= 70 THEN 'C'
		ELSE 'F'
	END AS 학점
FROM dt_demo;

-- id, name, 홀짝 (id가 홀수면 홀)
SELECT
	id,
	name,
	CASE
		WHEN id % 2 = 1 THEN '홀'
		ELSE '짝'
	END AS 홀짝
FROM dt_demo;
