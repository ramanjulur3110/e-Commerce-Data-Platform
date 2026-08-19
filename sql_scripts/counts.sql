SELECT count(*), 'generator.orders' as table_name from generator.orders
UNION ALL
SELECT count(*),'generator.order_details' from generator.order_details
UNION ALL
SELECT count(*), 'generator.order_status_history' from generator.order_status_history
UNION ALL 
SELECT count(*), 'generator.payment_orders' from generator.payment_orders
UNION ALL
SELECT count(*), 'generator.payment_orders_state_history' from generator.payment_status_history;

SELECT count(*), 'generator.customers' as table_name from generator.customers
UNION ALL
SELECT count(*),'generator.payment_type' from generator.payment_type
UNION ALL
SELECT count(*), 'generator.product_categories' from generator.product_categories
UNION ALL 
SELECT count(*), 'generator.product_subcategories' from generator.product_subcategories
UNION ALL
SELECT count(*), 'generator.products' from generator.products
UNION ALL
SELECT count(*), 'generator.ref_shipping_rates' from generator.ref_shipping_rates
UNION ALL
SELECT count(*), 'generator.ref_tax_rates' from generator.ref_tax_rates

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
WHERE payment_order_id in ('343440')
order by payment_order_id ASC, created_at DESC;

select count(order_id), order_status 
from generator.orders
group by order_status;

SELECT * from generator.payment_orders
where payment_status <> 'APPROVED'
order by order_id ASC;

select 
    * , ROUND((order_count / total_orders) * 100, 2) || '%' as percent_total
from (
    SELECT count(order_id) as order_count, failure_reason, SUM(count(order_id)) OVER () as total_orders
    from generator.payment_orders
    where payment_status = 'DECLINED'
    and failure_reason != 'MAX_RETRY_ATTEMPTS_EXCEEDED'
    group by failure_reason
    order by order_count DESC
) as subquery

select count(o.order_id), o.order_status, p.payment_status
from generator.orders o
left join generator.payment_orders p
    on o.order_id = p.order_id
group by o.order_status, p.payment_status


-- SELECT distinct count(*) from generator.payment_status_history
SELECT count(distinct payment_order_id) from generator.payment_status_history
where payment_order_id in 
    (
    select payment_order_id from generator.payment_orders
    where payment_status in ('PROCESSING', 'TIMEOUT') 
    )
-- group by payment_order_id
-- order by payment_order_id
-- select order_id from generator.payment_orders
-- where payment_status in ('PROCESSING', 'TIMEOUT')

select count(distinct order_id) from generator.order_status_history
where order_id in 
    (
    select order_id from generator.payment_orders
    where payment_status in ('PROCESSING', 'TIMEOUT') 
    )
