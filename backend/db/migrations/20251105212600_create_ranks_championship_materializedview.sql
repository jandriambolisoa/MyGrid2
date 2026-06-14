-- migrate:up
CREATE MATERIALIZED VIEW public.ranks_championships_mv
AS
WITH ranked_scores AS (
	SELECT scores.user_id,
	scores.session_id,
	championships.id AS championship_id,
	SUM(scores.score) AS score,
	ROW_NUMBER() OVER (
		PARTITION BY user_id, championships.id
		ORDER BY SUM(scores.score) DESC
	) AS session_rank
	FROM scores
	LEFT JOIN sessions ON sessions.id = scores.session_id
	LEFT JOIN events ON events.id = sessions.event_id
	LEFT JOIN championships ON championships.id = events.championship_id
	GROUP BY championships.id, scores.user_id, scores.session_id
	ORDER BY score DESC
	)
SELECT championships.id AS championship_id,
users.id AS user_id,
COALESCE(SUM(ranked_scores.score), 0) AS score,
ROW_NUMBER() OVER (
	PARTITION BY championships.id
	ORDER BY SUM(ranked_scores.score) DESC
	) AS rank,
STRING_AGG(ranked_scores.session_id::TEXT, ',' ORDER BY ranked_scores.score DESC) AS session_list
FROM ranked_scores
LEFT JOIN users ON users.id = ranked_scores.user_id
LEFT JOIN sessions ON sessions.id = ranked_scores.session_id
LEFT JOIN events ON events.id = sessions.event_id
LEFT JOIN championships ON championships.id = events.championship_id
WHERE ranked_scores.session_rank <= 8
GROUP BY championships.id, users.id
ORDER BY score DESC
WITH DATA;


-- migrate:down
DROP MATERIALIZED VIEW IF EXISTS public.ranks_championships_mv;
