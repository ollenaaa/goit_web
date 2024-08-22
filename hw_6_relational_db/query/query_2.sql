select st.id, st.name, avg(sc.score) as avg_grade
from student as st
right join score as sc on sc.student_id_fn = st.id
left join lesson as l on sc.lesson_id_fn = l.id
where l.lesson = 'Animator'
group by st.id, st.name
order by avg_grade desc
limit 1