drop table if exists posts;
create table posts (
  id integer primary key autoincrement,
  title text not null,
  'text' text not null,
  created_at real not null
);