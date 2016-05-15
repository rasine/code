# -*- coding=UTF-8 -*-
#fun:记录常用的函数

# fun：交换参数
def chenage2Elements(a,b):
	a=b-a
	#b=b-(b-a) = a
	b=b-a
	#a=a+(b-a) = b
	a=b+a
	return a,b



