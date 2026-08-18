def reset_batch_metadata(batch_metadata):
    batch_metadata['order_insert_tuple'] = []
    batch_metadata['order_details_insert_tuple_start'] = []
    batch_metadata['order_details_insert_tuple_final'] = []
    batch_metadata['number_insert'] = 0
    batch_metadata['update_dict'] = {}