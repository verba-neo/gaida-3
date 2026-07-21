-- 03-insert.sql

INSERT INTO members (name, email, age)
VALUES ('김김김', 'a@email.com', 30);

-- name NOT NULL 설정으로 오류
INSERT INTO members (age)
VALUES (50);

INSERT INTO members (name)
VALUES ('박박박');

INSERT INTO members (name, email)
VALUES 
('이이이', 'lee@lee.com'),
('최최최', 'choi@choi.com'),
('정정정', 'jung@jung.com');

-- 데이터 확인용
SELECT * FROM members;