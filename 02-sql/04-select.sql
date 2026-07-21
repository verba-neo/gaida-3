-- 04-select.sql

-- * -> 모든 컬럼
SELECT * FROM members;

-- 컬럼 지정
SELECT name, age FROM members;

-- 데이터 지정 -> 조건 필터링
SELECT * FROM members WHERE id=6;
SELECT * FROM members WHERE age=20;
SELECT * FROM members WHERE age>25;

-- 나이가 20인 사람들의 이름/나이 만 조회
SELECT name, age FROM members WHERE age=20;