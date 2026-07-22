-- p01.sql

-- 1. userinfo 테이블 생성
CREATE TABLE userinfo (
    -- id INT PK
	id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    -- nickname: 글자 20자 까지, 필수 입력
	nickname VARCHAR(20) NOT NULL,
    -- phone 글자 11 글자 까지, 중복 방지
	phone VARCHAR(11) UNIQUE,
    -- reg_date 날짜, 기본값(오늘 날짜)
	reg_date DATE DEFAULT CURRENT_DATE
);

-- 2. userinfo 테이블 CRUD
INSERT INTO userinfo (nickname, phone) VALUES
('alice', '0104567890'),
('bob', '0104561234'),
('charlie', '01112345678'),
('david', '01874562131'),
('eric', '01054687913');


-- 전체 조회 (중간중간 계속 실행하면서 모니터링) R
SELECT * FROM userinfo;
-- id 가 3인 사람 조회 R
SELECT * FROM userinfo WHERE id = 3;
-- 별명이 bob 인 사람을 조회 R
SELECT * FROM userinfo WHERE nickname = 'bob';
-- 별명이 bob 인 사람의 핸드폰 번호를 01099998888 로 수정 (id로 수정) U
UPDATE userinfo SET phone = '01099998888' WHERE nickname = 'bob';
-- 별명이 bob 인 사람 삭제 (id로 수정) D
DELETE FROM userinfo WHERE id=2;