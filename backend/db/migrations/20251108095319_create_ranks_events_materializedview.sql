-- migrate:up
CREATE MATERIALIZED VIEW public.ranks_events_mv
AS
SELECT events.id AS event_id,
championships.id AS championship_id,
users.id AS user_id,
COALESCE(SUM(scores.score), 0) AS score,
ROW_NUMBER() OVER (
	PARTITION BY events.id
	ORDER BY SUM(scores.score) DESC
	) AS rank
FROM scores
LEFT JOIN users ON users.id = scores.user_id
LEFT JOIN sessions ON sessions.id = scores.session_id
LEFT JOIN events ON events.id = sessions.event_id
LEFT JOIN championships ON championships.id = events.championship_id
GROUP BY events.id, championships.id, users.id
ORDER BY score DESC
WITH NO DATA;


-- migrate:down
DROP MATERIALIZED VIEW IF EXISTS public.ranks_events_mv;
