def validate_bin_data(data):
    if not isinstance(data, dict):
        return {'error': 'Data must be a dict'}
    if 'U_ID' not in data or not isinstance(data.get('U_ID', None), int):
        return {'error': 'key U_ID of type int must be present'}
    if 'URL' not in data or not isinstance(data.get('URL', None), basestring):
        return {'error': 'key URL of type string must be present'}
    if 'LEVEL' not in data or not isinstance(data.get('LEVEL', None), int):
        return {'error': 'key LEVEL of type int must be present'}
    if 'LAT' not in data or not isinstance(data.get('LAT', None), basestring):
        return {'error': 'key LAT of type string is required'}
    if 'LONG' not in data or not isinstance(data.get('LONG', None), basestring):
        return {'error': 'key LONG of type string is required'}
    if 'TIMESTAMP' not in data or not isinstance(data.get('TIMESTAMP', None), basestring):
        return {'error': 'key TIMESTAMP of type string is required'}
    if 'TAGS' not in data or not isinstance(data.get('TAGS', None), list):
        return {'error': 'key TAGS of type list is required'}

    return {'success': 'data validation successful'}
