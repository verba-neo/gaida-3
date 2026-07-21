-- 08-where.sql

CREATE TABLE students (
	id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	name VARCHAR(10),
	age INT
);

INSERT INTO students (name, age) VALUES
('김민둥산', 22);



SELECT * FROM students;

-- 특정 컬럼의 값
-- 같음 (=)
SELECT * FROM students WHERE name = '황정민';
-- 다름 (!=)
SELECT * FROM students WHERE name != '김철수';
-- 이상 (>=)
SELECT * FROM students WHERE age >= 22;
-- 초과 (>)
SELECT * FROM students WHERE age > 23;
-- 범위 (이상-이하)
SELECT * FROM students WHERE age BETWEEN 21 AND 24;
-- 다중 선택
SELECT * FROM students WHERE name = '이영희' AND age = 20;
SELECT * FROM students WHERE id = 1 OR age = 20 OR age = 21;
SELECT * FROM students WHERE id IN (1, 3, 5);

-- 텍스트 패턴 LIKE (% -> 있을수도/없을수도, _ -> 개수만큼 있다)
-- '최' 시작
SELECT * FROM students WHERE name LIKE '최%';
-- '범' 끝남
SELECT * FROM students WHERE name LIKE '%범';
-- '민' 있음
SELECT * FROM students WHERE name LIKE '%민%';

-- '범' 앞에 반드시 글자 2개
SELECT * FROM students WHERE name LIKE '__범';
-- '민' 이 가운데 글자
SELECT * FROM students WHERE name LIKE '_민_';

-- 성 말고, 이름의 첫글자가 '민'
SELECT * FROM students WHERE name LIKE '_민%';











