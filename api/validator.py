from telegram import send_asynch_message as sam


def validate_bin_data(data):
    if not isinstance(data, dict):
        return {'error': 'Data must be a dict'}
    if 'U_ID' not in data or not isinstance(data.get('U_ID', None), basestring):
        return {'error': 'key U_ID of type string must be present'}
    if 'USER_NAME' not in data or not isinstance(data.get('USER_NAME', None), basestring):
        return {'error': 'key USER_NAME of type string must be present'}
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

    classifier = dict()
    classifier['banana'] = "biodegradable"
    classifier['plastic'] = "non-biodegradable"

    bio = 0
    nonbio = 0
    stag = ""
    for tag in data['TAGS']:
        if tag in classifier.keys() and classifier.get(tag) == "biodegradable":
            bio += 1
            stag = tag
        if tag in classifier.keys() and classifier.get(tag) == "non-biodegradable":
            nonbio += 1
            stag = tag

    if bio > nonbio and 'TYPE' in data and data['TYPE'] == "1":
        sam.send_message("piyush9620",
                         stag + " : Dear user, you have put the waste in the wrong dustbin, plz put it in the biodegradable waste bin as " + stag + " is classified as biodegradable")

    if bio < nonbio and 'TYPE' in data and data['TYPE'] == "0":
        sam.send_message("piyush9620",
                         stag + " : Dear user, you have put the waste in the wrong dustbin, plz put it in the non-biodegradable waste bin as " + stag + " is classified as non-biodegradable")

    return {'success': 'data validation successful'}
