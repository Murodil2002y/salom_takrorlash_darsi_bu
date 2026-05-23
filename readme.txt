before using my code you need to install postgresql and pgAdmin4 and read requirements.txt
```````````````````````````````````````````````````````````````````````````````````````````

sql codes
```````````````````````````````````````````````````````````````````````````````````````````

DB_HOST=localhost
DB_PORT=5432
DB_NAME=
DB_USER=
DB_PASSWORD=

````````````````````````````````````````````````````````````````````````````````````````````````
-- Mualliflar jadvali
CREATE TABLE authors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- Kitoblar jadvali (Muallifga bog'langan va kamaymaydigan cheklovga ega)
CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author_id INTEGER,
    available_copies INTEGER DEFAULT 0,
    CONSTRAINT fk_books_authors FOREIGN KEY (author_id) REFERENCES authors(id) ON DELETE CASCADE,
    CONSTRAINT chk_available_copies CHECK (available_copies >= 0)
);

-- Bot foydalanuvchilari jadvali
CREATE TABLE bot_users (
    telegram_id BIGINT PRIMARY KEY,
    full_name VARCHAR(255),
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


INSERT INTO authors (name) VALUES
('Abdulla Qodiriy'),
('O''tkir Hoshimov'),
('Tohir Malik');

INSERT INTO books (title, author_id, available_copies) VALUES
('O''tkan kunlar', 1, 5),
('Mehrobdan chayon', 1, 0), -- Sinov uchun nusxasi qolmagan qildik (5-topshiriq logikasi uchun)
('Dunyoning ishlari', 2, 7),
('Ikki eshik orasi', 2, 4),
('Shaytanat', 3, 2);

````````````````````````````````````````````````````````````````````````````````````````````````````````````