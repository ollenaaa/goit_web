select g.name, st.name, l.lesson, s.score
from groupe g
inner join student st on st.groupe_id_fn = g.id
right join score s on s.student_id_fn = st.id
left join lesson l on l.id = s.lesson_id_fn
where l.lesson = 'Producer, radio' and g.name = 'Walker-Lopez'