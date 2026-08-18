SELECT count(*), 'generator.orders' as table_name from generator.orders
UNION ALL
SELECT count(*),'generator.order_details' from generator.order_details
UNION ALL
SELECT count(*), 'generator.order_status_history' from generator.order_status_history
UNION ALL 
SELECT count(*), 'generator.payment_orders' from generator.payment_orders
UNION ALL
SELECT count(*), 'generator.payment_orders_state_history' from generator.payment_status_history;


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

select count(od.product_id)as count, p.shipping_class
from generator.order_details od
LEFT JOIN generator.products p
    on p.product_id = od.product_id
group by p.shipping_class;

SELECT * from generator.orders
order by order_id ASC;
SELECT * from generator.order_details
order by order_id ASC;
SELECT * from generator.order_status_history
order by order_id ASC, order_status DESC;
SELECT * from generator.payment_orders
order by order_id ASC;
SELECT *from generator.payment_status_history
WHERE payment_order_id in ('83')
order by payment_order_id ASC, created_at DESC;

select count(order_id), order_status 
from generator.orders
group by order_status;

SELECT * from generator.payment_orders
where payment_status <> 'APPROVED'
order by order_id ASC;