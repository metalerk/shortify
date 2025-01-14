CREATE TABLE IF NOT EXISTS urls (
    id SERIAL PRIMARY KEY,
    shortcode VARCHAR(255) NOT NULL UNIQUE,
    url TEXT NOT NULL,
    update_id UUID NOT NULL UNIQUE,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_redirect TIMESTAMP,
    redirect_count INT DEFAULT 0
);

INSERT INTO urls (shortcode, url, update_id, created, last_redirect, redirect_count)
VALUES
('test123', 'https://www.example.com', '11111111-1111-1111-1111-111111111111', NOW(), NULL, 0)
ON CONFLICT DO NOTHING;
