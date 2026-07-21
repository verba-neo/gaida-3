-- 06-delete.sql

SELECT * FROM members;

-- 테이블에서 특정 데이터 삭제
DELETE FROM members WHERE id=4;

-- **위험** 테이블의 모든 데이터 삭제
DELETE FROM members;