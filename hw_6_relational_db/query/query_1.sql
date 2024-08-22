select st.id, st.name, avg(sc.score) as avg_score 
from student as st 
left join score as sc on sc.student_id_fn = st.id 
group by st.id, st.name 
order by avg_score desc
limit 5