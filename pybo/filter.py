import locale
locale.setlocale(locale.LC_ALL, '') #  UnicodeEncodeError 오류가 발생시 사용

def format_datetime(value, fmt='%Y년 %m월 %d일 %p %I:%M'):  # H는 24시간제  %S	초  %f	마이크로초
    return value.strftime(fmt) # 날짜포맷형식(fmt)에 맞게 변환하여 리턴

#
# 전체 게시물개수   -    (현재 페이지 - 1)   *  페이지당 게시물 개수 - 나열 인덱스
#       22                 1/0                   10                 0  1  2  3  4  5  6  7  8  9
#                                                                  22 21 20 19 18  17 16 15 14 13
#       22                 2/1                   10                 0  1  2  3  4  5  6  7  8  9
#                                                                  12 11 10  9  8  7  6  5  4  3
#       22                 3/2                   10                 0  1
#                                                                   2  1