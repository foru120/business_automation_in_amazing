def constant(func):
    def func_set(self, value):
        raise TypeError

    def func_get(self):
        return func()

    return property(func_get, func_set)


class _Const(object):
    @constant
    def URL_KCDCODE():
        return 'https://www.kcdcode.kr/browse/contents/0'

    @constant
    def CODE_DISEASE_CLASSIFICATION():
        return '질병분류코드'


CONST = _Const()