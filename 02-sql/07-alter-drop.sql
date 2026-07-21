-- 07-alter-drop.sql
-- 테이블 컬럼의 수정/삭제

-- 컬럼 추가
ALTER TABLE members
ADD COLUMN address VARCHAR(100) NOT NULL DEFAULT '';

-- 컬럼 이름 수정
ALTER TABLE members
RENAME COLUMN address TO juso;

-- 컬럼 타입 수정
ALTER TABLE members
ALTER COLUMN juso TYPE TEXT;

ALTER TABLE members
ALTER COLUMN age SET DEFAULT 10;

-- 컬럼 삭제
ALTER TABLE members
DROP COLUMN email;

SELECT * FROM members;




