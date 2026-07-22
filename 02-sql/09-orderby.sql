-- 09-orderby.sql

-- students 테이블 생성
DROP TABLE IF EXISTS students;

CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    name VARCHAR(30) NOT NULL,
    age INT NOT NULL
);

-- 데이터 입력
INSERT INTO students (name, age) VALUES
('김민수', 25),
('이서연', 22),
('박지훈', 30),
('최유진', 28),
('정다은', 35),
('한지민', 27),
('오세훈', 24),
('강하늘', 31),
('윤아름', 29),
('신현우', 26),
('조수빈', 21),
('백지훈', 33),
('임도윤', 38),
('문서준', 24),
('장예린', 40),
('홍길동', 37),
('노지훈', 23),
('서민재', 28),
('고은별', 34),
('유지호', 36),
('송하윤', 32),
('양준혁', 27),
('권소희', 39),
('안재현', 25),
('배수지', 29),
('남도현', 26),
('진예린', 30),
('심지호', 22),
('차은우', 24),
('황민지', 35);

-- grade 컬럼을 추가. VARCHAR(1) DEFAULT 'B'
ALTER TABLE students 
ADD COLUMN grade VARCHAR(1) DEFAULT 'B';
-- 일괄 데이터 수정
UPDATE students SET grade = 'A' WHERE id BETWEEN 1 AND 10;
UPDATE students SET grade = 'C' WHERE id BETWEEN 21 AND 30;

SELECT * FROM students;

-- id 순으로 정렬
-- ASC 오름차순 | DESC 내림차순
SELECT * FROM students ORDER BY id;
SELECT * FROM students ORDER BY id DESC;
-- 숫자
SELECT * FROM students ORDER BY age DESC;
-- 글자
SELECT * FROM students ORDER BY name ASC;

-- 다중 컬럼 정렬
SELECT * FROM students ORDER BY age DESC, grade ASC;
SELECT * FROM students ORDER BY grade ASC, age DESC, name;

-- 개수 제한
SELECT * FROM students ORDER BY grade LIMIT 5;

-- 나이가 25 이상인 학생들 중에
-- 학점이 가장 높은 사람을 나이 내림차순으로 5명의 이름만
SELECT name FROM students
WHERE age >= 25
ORDER BY grade ASC, age DESC
LIMIT 5;









