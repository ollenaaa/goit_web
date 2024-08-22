select distinct l.lesson
from teacher t
inner join lesson l on l.teacher_id_fn = t.id
inner join score sc on l.id = sc.lesson_id_fn
inner join student s on s.id = sc.student_id_fn
where s.name = 'Elizabeth Glover' and t.name = 'Jasmine Reese'