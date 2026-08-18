SELECT count(*) from generator.orders
UNION ALL
SELECT count(*) from generator.order_details
UNION ALL 
SELECT count(*) from generator.payment_orders
UNION ALL
SELECT count(*) from generator.payment_orders_state_history;

select 
    * , ROUND((order_count / total_orders) * 100, 2) || '%' as percent_total
from (
    SELECT count(po.payment_order_id) as order_count, po.payment_type_id, pt.payment_type, sum(count(po.payment_order_id)) OVER () as total_orders
    from generator.payment_orders po
    left join generator.payment_type pt 
        on pt.payment_type_id = po.payment_type_id
    group by po.payment_type_id, pt.payment_type
    order by count(po.payment_order_id) DESC
) as subquery
