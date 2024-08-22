select sc.score, max(sc.date)
from groupe g
right join student s on g.id = s.groupe_id_fn
inner join score sc on s.id = sc.student_id_fn
left join lesson l on l.id = sc.lesson_id_fn
where g.name = 'Chen, Sutton and Huang' and l.lesson = 'Air broker'