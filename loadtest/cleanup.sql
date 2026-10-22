DELETE FROM click_events
WHERE link_id IN (
  SELECT id FROM links WHERE original_url LIKE 'https://93.184.216.34/loadtest/%'
);

DELETE FROM links
WHERE original_url LIKE 'https://93.184.216.34/loadtest/%';
