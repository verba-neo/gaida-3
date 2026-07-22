-- 10-datatype.sql

DROP TABLE IF EXISTS dt_demo;

CREATE TABLE dt_demo(
	id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	name VARCHAR(20),  -- 20자 이하의 글자
	birth DATE,  -- YYYY-MM-DD
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- 날짜 + 시간, 자동 저장
	score FLOAT,  			-- 소수점 포함. 정확도 100% 아님.
	salary DECIMAL(20, 3),  -- 전체 20자리 숫자, 뒤에 3자리는 소숫점, 정확도 100%
	bio TEXT,  				-- 길이제한이 없는 문자열
	is_married BOOL DEFAULT FALSE  -- 참/거짓
);

INSERT INTO dt_demo (name,  birth, score, salary, bio)
VALUES
('김철수', '1995-01-01', 88.75, 3500000, '우수한 학생입니다.'),
('이영희', '1990-05-15', 92.30, 4200000.8888, '성실하고 열심히 공부합니다.'),
('박민수', '1988-09-09', 75.80, 2800000.75, '기타 사항 없음');

SELECT * FROM dt_demo;