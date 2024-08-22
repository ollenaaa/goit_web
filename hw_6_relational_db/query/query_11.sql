select avg(sc.score) as avg_score
from teacher t
right join lesson l on t.id = l.teacher_id_fn
join score sc on l.id = sc.lesson_id_fn
left join student s on s.id = sc.student_id_fn
where s.name = 'Troy Cooley' and t.name = 'Robert Bentley'