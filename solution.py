_header_cache = {}


def _normalize_data(data: str) -> str:
    return data.replace('\r\n', '\n').replace('\r', '\n')


def _parse_header(data: str) -> tuple:
    newline_pos = data.index('\n')
    header_line = data[:newline_pos]
    columns = header_line.split(',')
    column_indexes = {col: idx for idx, col in enumerate(columns)}
    value_index = column_indexes['value']
    return column_indexes, value_index, newline_pos + 1


def _get_cached_header(data: str) -> tuple:
    global _header_cache
    newline_pos = data.index('\n')
    header_key = data[:newline_pos]
    if header_key not in _header_cache:
        _header_cache[header_key] = _parse_header(data)
    return _header_cache[header_key]


def task1(search: dict, data: str) -> str:
    data = _normalize_data(data)
    column_indexes, value_index, data_start = _get_cached_header(data)
    
    for key in search:
        if key not in column_indexes:
            raise Exception("Key mismatch")
    
    search_pairs = [(column_indexes[k], str(v)) for k, v in search.items()]
    
    pos = data_start
    data_len = len(data)
    
    while pos < data_len:
        newline_pos = data.find('\n', pos)
        if newline_pos == -1:
            newline_pos = data_len
        
        if newline_pos == pos:
            pos = newline_pos + 1
            continue
        
        line = data[pos:newline_pos]
        pos = newline_pos + 1
        
        values = line.split(',')
        
        match = True
        for col_idx, expected_val in search_pairs:
            if col_idx >= len(values) or values[col_idx] != expected_val:
                match = False
                break
        
        if match:
            return values[value_index]
    
    return '-1'


def task2(search_list: list, data: str) -> str:
    data = _normalize_data(data)
    column_indexes, value_index, data_start = _get_cached_header(data)
    
    for search in search_list:
        for key in search:
            if key not in column_indexes:
                raise Exception("Key mismatch")
    
    search_conditions = []
    for search in search_list:
        pairs = tuple((column_indexes[k], str(v)) for k, v in search.items())
        search_conditions.append(pairs)
    
    found_indices = set()
    found_values = []
    num_searches = len(search_conditions)
    
    pos = data_start
    data_len = len(data)
    
    while pos < data_len and len(found_indices) < num_searches:
        newline_pos = data.find('\n', pos)
        if newline_pos == -1:
            newline_pos = data_len
        
        if newline_pos == pos:
            pos = newline_pos + 1
            continue
        
        line = data[pos:newline_pos]
        pos = newline_pos + 1
        
        values = line.split(',')
        
        for search_idx, search_pairs in enumerate(search_conditions):
            if search_idx in found_indices:
                continue
            
            match = True
            for col_idx, expected_val in search_pairs:
                if col_idx >= len(values) or values[col_idx] != expected_val:
                    match = False
                    break
            
            if match:
                found_indices.add(search_idx)
                found_values.append(int(values[value_index]))
    
    if not found_values:
        return "0.0"
    
    weighted_sum = 0
    total_weight = 0
    
    for value in found_values:
        weight = 10 if value % 2 == 1 else 20
        weighted_sum += value * weight
        total_weight += weight
    
    if total_weight == 0:
        return "0.0"
    
    result = weighted_sum / total_weight
    return f"{result:.1f}"
