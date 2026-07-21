-- 05-update.sql

-- name 이 '익명' 인 사용자를 추가
INSERT INTO members (name) VALUES ('익명');

SELECT * FROM members;

UPDATE members
SET age=25
WHERE name='익명';

-- 특정 데이터 row 를 수정할 때, id로 선택하는것이 일반적

-- 마지막 사람의 email 과 이름 수정
UPDATE members
SET name='홍길동', email='hong@gil.dong'
WHERE id=9;

-- *주의* 나이가 20살인 사람들 모두 21살로 바꾸기
UPDATE members
SET age=21
WHERE age=20;
