-- p03.sql

DROP TABLE IF EXISTS userinfo;

CREATE TABLE userinfo (
	id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	name VARCHAR(100),
	phone VARCHAR(11) UNIQUE,
    email VARCHAR(40)
);

INSERT INTO userinfo (name, phone, email) VALUES
('김지멜', '01115545378', 'kim@gmail.com'),
('김철수', '01112345378', 'kim@test.com'),
('이영희', NULL, 'lee@gmail.com'),
('정수민', '01012347788', 'chong@gmail.com'),
('박민수', '01012345637', NULL),
('최영수', '01745367894', 'choi@naver.com');

SELECT * FROM userinfo;

-- id 가 3 이상인 사용자
SELECT * FROM userinfo WHERE id >= 3;
-- email 이 gmail.com 이거나 naver.com 특정 도메인으로 끝나는 사용자들
SELECT * FROM userinfo WHERE email 
LIKE '%gmail.com' OR email LIKE '%naver.com';
-- 이름이 김철수, 박민수 2명 뽑기
SELECT * FROM userinfo WHERE name='김철수' OR name='박민수';
SELECT * FROM userinfo WHERE name IN ('김철수', '박민수', 'ㅋㅋㅋㅋ');
-- 이메일이 비어있는(NULL) 사람들 -> is NULL
SELECT * FROM userinfo WHERE email IS NULL;
SELECT * FROM userinfo WHERE email IS NOT NULL;
-- 이름에 수 글자가 들어간 사람들
SELECT * FROM userinfo WHERE name LIKE '%수%';
-- 핸드폰 번호 010으로 시작하는 사람들
SELECT * FROM userinfo WHERE phone LIKE '010%';
-- 이름에 '수' 가 있고, 폰번호 010, gmail 쓰는 사람
SELECT * FROM userinfo WHERE 
name LIKE '%수%' AND 
phone LIKE '010%' AND
email LIKE '%gmail.com';

-- 성이 김/이 둘중 하난데 gmail 씀
SELECT * FROM userinfo WHERE
(name LIKE '김%' OR name LIKE '이%')  -- 연산자 우선순위 AND > OR
AND email LIKE '%gmail.com';
