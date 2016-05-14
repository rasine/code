# -*- coding=UTF-8 -*-
import sys

#这是添加的
#显示中文
reload(sys)
sys.setdefaultencoding('utf8')

class ClassTest(object):
	"""docstring for ClassTest"""
	data = ["value1","value2","value3"]
	x = 7

	def __init__(self,name,color):
		self.name = name
		self.color = color

	def sayHello(self):
		print "%s hello" %(self.name)

	def getName(self):
		return self.name

	def getColor(self):
		print self.color

test = ClassTest("rasine","red")
print ClassTest.x
print test.x
test.x += 1
print ClassTest.x
print test.x
del test.x
print ClassTest.x
print test.x
print dir(test)
print dir(ClassTest)
print globals()
