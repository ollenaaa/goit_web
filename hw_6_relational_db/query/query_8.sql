select t.name, avg(s.score) as avg_score
from teacher t
right join lesson l on t.id = l.teacher_id_fn
left join score s on s.lesson_id_fn = l.id
where t.name = 'Jason Bradley'