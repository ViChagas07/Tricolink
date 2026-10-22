INSERT INTO links (code, original_url, is_custom_alias, is_active, click_count)
SELECT
  'ld' || substr(md5(g::text || random()::text), 1, 5),
  'https://93.184.216.34/loadtest/redirect-' || g,
  false,
  true,
  0
FROM generate_series(1, 500) AS g
ON CONFLICT (code) DO NOTHING;
