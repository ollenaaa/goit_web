select s.id, s.name, g.name
from student s
left join groupe g on s.groupe_id_fn = g.id
where g.id = 2