year = int(input('year:'))
month = int(input('month:'))
day = int(input('day:'))                                 # 原解bug：日期可能不合理，例如2月的32号这样，原解并未检测
# 更改：增加一个新数组days，在输入日期后多一步判定2
months = (0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334)
days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
if (year % 400 == 0) or ((year % 4 == 0) and (year % 100 != 0)):  # 判断是否是闰年
    leap = 1
    days[1] = 29
if 0 < month <= 12 and day <= days[month-1]:
    sum = months[month-1]
    sum += day
    leap = 0

    if (leap == 1) and (month > 2):
        sum += leap
    print('it is the %dth day' % sum)
else:
    print('data error')

