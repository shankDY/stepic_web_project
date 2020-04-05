def app(environ, start_response):
    """парсим часть url, которая поступает после ?. например /?value=a=1&b=3, получаем список"""
    data = [bytes('\n'.join(environ['QUERY_STRING'].split('&')), encoding='utf8')]
    #статус код
    status = '200 OK'
    #заголовок ответа
    response_headers = [
        ('Content-type', 'text/plain'),
        ('Content-Length', str(len(data)))
    ]
    #вызов функции start_response
    start_response(status, response_headers)
    # возвращаем список с данными из части урла после ?
    return data