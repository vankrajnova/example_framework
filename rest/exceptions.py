def error_by_status_code(status_code: int):
    dict_codes = {
        400: BadRequestException,
        401: UnauthorizedException,
        403: ForbiddenException,
        404: NotFoundException,
        405: MethodNotAllowedException,
        406: NotAcceptableException,
        407: ProxyAuthenticationRequiredException,
        408: RequestTimeoutException,
        409: ConflictException,
        410: GoneException,
        411: LengthRequiredException,
        412: PreconditionFailedException,
        413: RequestEntityTooLargeException,
        414: Request_URI_TooLongException,
        415: UnsupportedMediaTypeException,
        416: RequestedRangeNotSatisfiableException,
        417: ExpectationFailedException,
        500: InternalServerErrorException,
        501: NotImplementedException,
        502: BadGatewayException,
        503: ServiceUnavailableException,
        504: GatewayTimeoutException,
        505: HTTPVersionNotSupportedException,
    }
    if (status_code // 100) in [4, 5]:
        exception = dict_codes.get(status_code)
        if exception is None:
            if (status_code // 100) == 4:
                exception = ClientException(status_code)
            else:
                exception = ServerException(status_code)
        return exception
    else:
        return None


# 4xx


class ClientException(Exception):

    def __init__(self, code=None):
        Exception.__init__(
            self,
            f"На стороне клиента произошла ошибка (4XX) - {code}"
        )


class BadRequestException(Exception):

    def __init__(self):
        Exception.__init__(
            self,
            '400. "Плохой запрос". '
            'Этот ответ означает, что сервер не понимает запрос из-за неверного синтаксиса.',
        )


class UnauthorizedException(Exception):

    def __init__(self):
        Exception.__init__(
            self,
            '401. "Не авторизованно". '
            'Для получения запрашиваемого ответа нужна аутентификация. Статус похож на статус 403, но,в этом случае, '
            'аутентификация возможна.',
        )


class ForbiddenException(Exception):

    def __init__(self):
        Exception.__init__(
            self,
            '403. "Запрещено". '
            'У клиента нет прав доступа к содержимому, поэтому сервер отказывается дать надлежащий ответ.',
        )


class NotFoundException(Exception):

    def __init__(self):
        Exception.__init__(
            self,
            '404. "Не найден". '
            'Сервер не может найти запрашиваемый ресурс.',
        )


class MethodNotAllowedException(Exception):

    def __init__(self):
        Exception.__init__(
            self,
            '405. "Метод не разрешён". '
            'Сервер знает о запрашиваемом методе, но он был деактивирован и не может быть использован.',
        )


class NotAcceptableException(Exception):

    def __init__(self):
        Exception.__init__(
            self,
            '406. '
            'Этот ответ отсылается, когда веб сервер после выполнения server-driven content negotiation, '
            'не нашёл контента, отвечающего критериям, полученным из user agent.',
        )


class ProxyAuthenticationRequiredException(Exception):

    def __init__(self):
        Exception.__init__(
            self,
            '407. Этот код ответа аналогичен коду 401, только аутентификация требуется для прокси сервера.',
        )


class RequestTimeoutException(Exception):

    def __init__(self):
        Exception.__init__(
            self,
            '408. '
            'Ответ с таким кодом может прийти, даже без предшествующего запроса. '
            'Он означает, что сервер хотел бы отключить это неиспользуемое соединение. '
            'Этот метод используется все чаще с тех пор, как некоторые браузеры, вроде Chrome и IE9, '
            'стали использовать HTTP механизмы предварительного соединения для ускорения сёрфинга',
        )


class ConflictException(Exception):

    def __init__(self):
        Exception.__init__(
            self,
            '409. Этот ответ отсылается, когда запрос конфликтует с текущим состоянием сервера.',
        )


class GoneException(Exception):

    def __init__(self):
        Exception.__init__(
            self,
            '410. Этот ответ отсылается, когда запрашиваемый контент удалён с сервера.',
        )


class LengthRequiredException(Exception):

    def __init__(self):
        Exception.__init__(
            self,
            '411. Запрос отклонён, потому что сервер требует указание заголовка Content-Length, но он не указан.',
        )


class PreconditionFailedException(Exception):

    def __init__(self):
        Exception.__init__(
            self,
            '412. Клиент указал в своих заголовках условия, которые сервер не может выполнить',
        )


class RequestEntityTooLargeException(Exception):

    def __init__(self):
        Exception.__init__(
            self,
            '413. '
            'Размер запроса превышает лимит, объявленный сервером. '
            'Сервер может закрыть соединение, вернув заголовок Retry-After',
        )


class Request_URI_TooLongException(Exception):

    def __init__(self):
        Exception.__init__(
            self,
            '414. URI запрашиваемый клиентом слишком длинный для того, чтобы сервер смог его обработать',
        )


class UnsupportedMediaTypeException(Exception):

    def __init__(self):
        Exception.__init__(
            self,
            '415. Медиа формат запрашиваемых данных не поддерживается сервером, поэтому запрос отклонён',
        )


class RequestedRangeNotSatisfiableException(Exception):

    def __init__(self):
        Exception.__init__(
            self,
            '416. '
            'Диапазон указанный заголовком запроса Range не может быть выполнен; возможно, он выходит за пределы '
            'переданного URI',
        )


class ExpectationFailedException(Exception):

    def __init__(self):
        Exception.__init__(
            self,
            '417. '
            'Этот код ответа означает, что ожидание, полученное из заголовка запроса Expect, не может быть выполнено '
            'сервером.',
        )


# 5xx

class ServerException(Exception):

    def __init__(self, code=None):
        Exception.__init__(
            self,
            f"На стороне сервера произошла ошибка (5XX) - {code}"
        )


class InternalServerErrorException(Exception):

    def __init__(self):
        Exception.__init__(
            self,
            '500. "Внутренняя ошибка сервера". Сервер столкнулся с ситуацией, которую он не знает как обработать.',
        )


class NotImplementedException(Exception):

    def __init__(self):
        Exception.__init__(
            self,
            '501. "Не выполнено". Метод запроса не поддерживается сервером и не может быть обработан. '
            'Единственные методы, которые сервера должны поддерживать (и, соответственно, не должны возвращать этот '
            'код) - GET и HEAD.',
        )


class BadGatewayException(Exception):

    def __init__(self):
        Exception.__init__(
            self,
            '502. "Плохой шлюз". '
            'Эта ошибка означает что сервер, во время работы в качестве шлюза для получения ответа, '
            'нужного для обработки запроса, получил недействительный (недопустимый) ответ.',
        )


class ServiceUnavailableException(Exception):

    def __init__(self):
        Exception.__init__(
            self,
            '503. "Сервис недоступен". '
            'Сервер не готов обрабатывать запрос. Зачастую причинами являются отключение сервера или то, '
            'что он перегружен. '
        )


class GatewayTimeoutException(Exception):

    def __init__(self):
        Exception.__init__(
            self,
            '504. '
            'Этот ответ об ошибке предоставляется, когда сервер действует как шлюз и не может получить ответ вовремя.'
        )


class HTTPVersionNotSupportedException(Exception):

    def __init__(self):
        Exception.__init__(
            self,
            '505. "HTTP-версия не поддерживается". HTTP-версия, используемая в запросе, не поддерживается сервером.'
        )


# ???

class AccessDeniedException(Exception):

    def __init__(self):
        Exception.__init__(
            self, "Доступ запрещен"
        )


class AccessAllowedException(Exception):

    def __init__(self):
        Exception.__init__(
            self, "Действие разрешено, хотя должно быть запрещено"
        )
