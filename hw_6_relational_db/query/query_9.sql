select distinct s.name, l.lesson
from student s
inner join score sc on sc.student_id_fn  = s.id
inner join lesson l on l.id = sc.lesson_id_fn
where s.id = 1
