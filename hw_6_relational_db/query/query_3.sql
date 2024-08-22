select g.id, g.name, avg(s.score) as avg_score
from groupe g
inner join student st on g.id = st.groupe_id_fn
right join score s on st.id = s.student_id_fn
inner join lesson l on l.id = s.lesson_id_fn
where l.lesson = 'Designer, graphic'
group by g.id, g.name
