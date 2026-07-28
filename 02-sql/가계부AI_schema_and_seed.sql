DROP TABLE IF EXISTS transaction_tags CASCADE;
DROP TABLE IF EXISTS transactions CASCADE;
DROP TABLE IF EXISTS recurring_expenses CASCADE;
DROP TABLE IF EXISTS tags CASCADE;
DROP TABLE IF EXISTS categories CASCADE;

-- 1. 카테고리 (기능 2, 6: 이름 + 선택적 예산 한도)
CREATE TABLE categories (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    monthly_budget NUMERIC(12, 0)  -- NULL이면 예산 한도 없음
);

-- 2. 반복 지출 정의 (기능 8: "넷플릭스 15900원 매달 27일" 같은 규칙)
CREATE TABLE recurring_expenses (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    amount NUMERIC(12, 0) NOT NULL,
    category_id INTEGER NOT NULL REFERENCES categories(id),
    billing_day INTEGER NOT NULL CHECK (billing_day BETWEEN 1 AND 31),
    start_date DATE NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);

-- 3. 실제 지출 기록 (기능 1, 4, 5)
-- recurring_expense_id: 반복 지출에서 자동 생성된 건이면 연결, 수동 입력이면 NULL
CREATE TABLE transactions (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    category_id INTEGER NOT NULL REFERENCES categories(id),
    recurring_expense_id INTEGER REFERENCES recurring_expenses(id),
    amount NUMERIC(12, 0) NOT NULL,
    memo VARCHAR(200),
    transaction_date DATE NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()  -- 기능 5: "가장 최근 입력" 판별용
);

-- 4. 태그 (기능 3)
CREATE TABLE tags (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

-- 5. 지출-태그 연결 (N:M)
CREATE TABLE transaction_tags (
    transaction_id INTEGER NOT NULL REFERENCES transactions(id) ON DELETE CASCADE,
    tag_id INTEGER NOT NULL REFERENCES tags(id) ON DELETE CASCADE,
    PRIMARY KEY (transaction_id, tag_id)
);

-- 중복 반복지출 기록 방지용 인덱스 (같은 달에 같은 recurring_expense_id 중복 방지 로직에서 활용)
CREATE INDEX idx_transactions_recurring_month
    ON transactions (recurring_expense_id, transaction_date);


-- ============================================
-- 더미 데이터
-- ============================================

-- 카테고리 (교통은 예산 없음 = 무제한)
INSERT INTO categories (name, monthly_budget) VALUES
('식비', 300000),
('교통', NULL),
('카페', 100000),
('구독', 50000),
('자기계발', 200000);

-- 반복 지출 정의
INSERT INTO recurring_expenses (name, amount, category_id, billing_day, start_date, is_active) VALUES
('넷플릭스', 15900, (SELECT id FROM categories WHERE name = '구독'), 27, '2026-01-27', TRUE),
('유튜브 프리미엄', 14900, (SELECT id FROM categories WHERE name = '구독'), 15, '2026-02-15', TRUE);

-- 태그
INSERT INTO tags (name) VALUES
('모임'), ('출장'), ('선물');

-- 지출 기록 (수동 입력 + 반복지출에서 생성된 것 섞어서)
INSERT INTO transactions (category_id, recurring_expense_id, amount, memo, transaction_date) VALUES
((SELECT id FROM categories WHERE name = '식비'), NULL, 15000, '점심', '2026-07-20'),
((SELECT id FROM categories WHERE name = '카페'), NULL, 4500, '커피', '2026-07-20'),
((SELECT id FROM categories WHERE name = '식비'), NULL, 32000, '팀 회식', '2026-07-21'),
((SELECT id FROM categories WHERE name = '교통'), NULL, 1500, '버스', '2026-07-22'),
((SELECT id FROM categories WHERE name = '자기계발'), NULL, 45000, '온라인 강의', '2026-07-23'),
((SELECT id FROM categories WHERE name = '식비'), NULL, 280000, '식비 초과 테스트용', '2026-07-24'),
((SELECT id FROM categories WHERE name = '구독'),
    (SELECT id FROM recurring_expenses WHERE name = '넷플릭스'), 15900, '넷플릭스 자동결제', '2026-06-27'),
((SELECT id FROM categories WHERE name = '구독'),
    (SELECT id FROM recurring_expenses WHERE name = '유튜브 프리미엄'), 14900, '유튜브 자동결제', '2026-07-15');

-- 지출-태그 연결 (같은 태그가 다른 카테고리 지출에도 붙는 케이스 포함)
INSERT INTO transaction_tags (transaction_id, tag_id) VALUES
((SELECT id FROM transactions WHERE memo = '팀 회식'), (SELECT id FROM tags WHERE name = '모임')),
((SELECT id FROM transactions WHERE memo = '커피'), (SELECT id FROM tags WHERE name = '모임')),
((SELECT id FROM transactions WHERE memo = '버스'), (SELECT id FROM tags WHERE name = '출장'));

SELECT * FROM transactions;
