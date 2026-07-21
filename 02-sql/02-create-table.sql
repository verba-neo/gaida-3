-- 02-create-table.sql

-- 테이블 이름, 컬럼 명/타입 -> 테이블 생성
CREATE TABLE sample (
	name VARCHAR(30),  -- 30글자 이하 (character)
	age INT            -- 정수(integer)
);

-- 테이블 삭제
DROP TABLE sample;

-- members 테이블 생성
CREATE TABLE members (
	-- 자동으로 배정되고, 1씩 올라가고, 해당 테이블의 가장 중요한 키(PK)
	id         INT          GENERATED ALWAYS AS IDENTITY,
	-- 30글자 이하, 비어있으면 안됨
	name       VARCHAR(30)  NOT NULL,
	-- 100글자 이하, 중복되면 안됨
	email      VARCHAR(100) UNIQUE,
	-- 데이터 기본값 20
	age        INT          DEFAULT 20,
	-- 자동으로 오늘 날짜
	join_date  DATE         DEFAULT CURRENT_DATE
);

DROP TABLE members;
