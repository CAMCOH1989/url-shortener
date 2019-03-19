CREATE TABLE IF NOT EXISTS urls(
    url_id serial PRIMARY KEY,
    url text not null,
    visited_at timestamp with time zone,
    created_at timestamp with time zone default clock_timestamp()
);



