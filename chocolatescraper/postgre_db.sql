CREATE DATABASE scraping;

\c scraping	                             # database 변경.


CREATE TABLE chocolate_products (
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    url VARCHAR(2083) NOT NULL
);

DROP TABLE chocolate_products;

-- table 의 권한 확인 및 수정
\dp chocolate_products

-- 권한이 부족한 경우, root 사용자에게 INSERT 권한을 부여
GRANT INSERT ON TABLE chocolate_products TO root;

-- chocolate_products 테이블의 소유자가 root인지 확인
SELECT tableowner FROM pg_tables WHERE tablename = 'chocolate_products';

-- root 사용자의 권한을 재확인
\du root

SELECT * FROM chocolate_products;