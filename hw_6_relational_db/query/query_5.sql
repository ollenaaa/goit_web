select t.id, t.name, l.lesson 
from teacher as t
left join lesson as l on l.teacher_id_fn = t.id
where t.name ='Jasmine Reese'
