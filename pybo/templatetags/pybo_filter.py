from django import template

# 템플릿 필터 : 템플릿 태그 안에 {변수|필터} 형식으로 되어있고, 값 변환 , 데이터 가공, 디폴트 값 설정 할때 사용된다. 장고에서 제공하지 않을 경우 함수로 만들어서 사용함.
# shift + 백 슬레시 = | ( 파이프 )
register = template.Library()


@register.filter
def sub(value, arg):
    return value - arg