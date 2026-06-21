-- p18 explode. string_split returns a list; unnest turns each list element into
-- its own row -> one (user_id, tag) per tag.
SELECT user_id, unnest(string_split(tags, ',')) AS tag
FROM user_tags;
