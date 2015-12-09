# -*- coding=UTF-8 -*-
from selenium import webdriver
import time
import sys

#显示中文
reload(sys)
sys.setdefaultencoding('utf8')

#截图
def screenShot(pic):
	browser.save_screenshot(pic)

#从配置文件中读取用户的cookie信息
def getCookieFromConfig():
	cookie = {}

	file_obj = open('cookie.txt')
	all_the_text = file_obj.read()
	file_obj.close()

	for x in xrange(0,len(all_the_text.split(";"))):
		cookie[all_the_text.split(";")[x].split("=")[0].strip()] = all_the_text.split(";")[x].split("=")[1]

	return cookie

#往w.midea.com域中写入配置的cookie信息
def addCookie2Domain(browser,cookies):
	for key in cookies:
		browser.add_cookie({'name':key,'value':cookies[key]})

#设备页面按钮
def deviceSwitch(cmd):
	if cmd == "switch":
		#开关按钮
		browser.find_element_by_xpath('//*[@id="js_switchBtn"]').click()
	elif cmd == "washinfo":
		#页面展示的洗衣模式
		return browser.find_element_by_xpath('//*[@id="js_infoTopTips"]').text
	elif cmd == "washstate":
		#页面显示设备状态：
		return browser.find_element_by_xpath('//*[@id="js_infoTips"]').text
	elif cmd == "pause":
		#获取页面暂停按钮信息
		return browser.find_element_by_css_selector('#js_pauseBtn').text
	elif cmd == "start":
		#获取页面启动按钮信息
		return browser.find_element_by_css_selector('#js_startLongBtn').text
	elif cmd == "washtime":
		#获取页面剩余工作时间
		return browser.find_element_by_css_selector('#js_countdown > div').text
	elif cmd == "startclick":
		#获取页面启动按钮信息
		browser.find_element_by_css_selector('#js_startLongBtn').click()
	elif cmd == "pauseclick":
		#页面暂停按钮
		browser.find_element_by_css_selector('#js_pauseBtn').click()
	elif cmd == "washstandard":
		#标准模式
		browser.find_element_by_xpath('//*[@id="js_washStandardBtn"]/i').click()
	elif cmd == "startshort":
		#初始启动按钮
		browser.find_element_by_xpath('//*[@id="js_startShortBtn"]').click()
	elif cmd == "babylock":
		js = '$("#js_babyLockBtn").trigger("tap")'
		browser.execute_script(js)
	else:
		print "err cmd :%s" %(cmd)


#查询设备状态
def queryDeviceState():
	jq = 'return $(".screen_wrap.off_mode .off_mode_cover").css("display")'
	display = browser.execute_script(jq)
	if display == None:
		return 1	#device is online!
	else:
		return 0	#device is not online

#获取童锁元素
def getElement4Babylock(element):
	return browser.find_element_by_css_selector('#js_babyLockBtn').get_attribute(element)

#测试用例----用户绑定设备列表页面是否正常拉取
def testCase4DeviceList():
	print "======== testCase4DeviceList ========"
	browser.get(url)
	li = browser.find_element_by_xpath('//*[@id="js_deviceListPage"]/div[3]').find_elements_by_tag_name('li')
	if len(li) != int(0):
		print "the user have %s devices" %(len(li))
	else:
		print "the user have %s devices" %(len(li))

	print "testcase ==> scuess"
	screenShot("./pic/deviceListScuess.png")

#测试用例----开机
def testCase4switchOpen4bolun():
	print "======== testCase4switchOpen4bolun ========"
	js = "return window.location.href;"
	print "currentUrl is %s" %(browser.execute_script(js))
	browser.find_element_by_xpath('//*[@id="js_deviceListPage"]/div[3]/ul/li[1]/div[1]').click()
	
	time.sleep(5)
	js = "return window.location.href;"
	print "currentUrl is %s" %(browser.execute_script(js))

	if queryDeviceState() == 1:
		print "errcode:%s ,errmsg:device initializing state is online!" %(queryDeviceState())
		print "switch first time"
		deviceSwitch('switch')
		time.sleep(2)
		print "switch second time"
		deviceSwitch('switch')
	else:
		print "errcode:%s ,errmsg:device initializing state is not online!" %(queryDeviceState())
		deviceSwitch('switch')

	time.sleep(5)
	print "errcode:%s,errmsg:device open!" %(queryDeviceState())
	print "testcase ==> scuess"
	screenShot("./pic/openDeviceScuess.png")

#测试用例----启动标准模式洗衣
def testCase4StandardRun4bolun():
	print "======== testCase4StandardRun4bolun ========"
	js = "return window.location.href;"
	print "currentUrl is %s" %(browser.execute_script(js))

	deviceSwitch('washstandard')
	deviceSwitch('startshort')

	#判断设备是否处于启动状态
	time.sleep(10)
	washinfo = deviceSwitch('washinfo')#标准
	washstate = deviceSwitch('washstate')#工作中···
	washtime = deviceSwitch('washtime')#工作时间 block
	btnstate = deviceSwitch("pause")#暂停

	if washinfo == "标准" and washstate == "工作中..." and washtime != "" and btnstate == "暂停":
		print "scuess,start device scuess! worklefttime:%s" %(washtime)
		print "testcase ==> scuess"
		screenShot("./pic/runWashstandardScuess.png")
	else:
		print "【err】：start device false,washinfo:%s washstate:%s washtime:%s btnstate:%s" %(washinfo,washstate,washtime,btnstate)
		print "testcase ==> false"

#测试用例----童锁
def testCase4Babylock4bolun():
	time.sleep(2)
	print "======== testCase4Babylock4bolun ========"
	babylockClassInfo = getElement4Babylock("class")

	if babylockClassInfo == "":
		print "device is running!"
		deviceSwitch("babylock")
		time.sleep(5)
		if getElement4Babylock("class") == "active":
			print "scuess,babylock device scuess!"
			screenShot("./pic/babylockScuess.png")

			#取消童锁
			while 1:
				print "begin cancel!"
				deviceSwitch("babylock")
				time.sleep(5)
				if getElement4Babylock("class") == "":
					print "scuess,cancel babylock scuess!"
					print "testcase ==> scuess"
					screenShot("./pic/cancelBabylockScuess.png")
					break
		else:
			print "【err】：babylock device false!"
			print "babylockstate:%s" %(getElement4Babylock("class"))
			print "testcase ==> false"
	elif babylockClassInfo == "hide":
		print "【err】：device is not running!"
		screenShot("./pic/babylockErr4Hide.png")
	elif babylockClassInfo == "active":
		print "【err】：device already babylock!"
		screenShot("./pic/babylockErr4Active.png")
	else:
		print "【err】：unknown err"
		screenShot("./pic/babylockErr4Unknown.png")

#测试用例----暂停标准模式洗衣
def testCase4StandardPause4bolun():
	print "======== testCase4StandardPause4bolun ========"
	btnstate = deviceSwitch("pause")
	if btnstate == "暂停":
		print "begin pause cmd!"
		deviceSwitch("pauseclick")

		#判断设备是否处于暂停状态
		time.sleep(10)
		washinfo = deviceSwitch('washinfo')#标准
		washstate = deviceSwitch('washstate')#暂停任务
		washtime = deviceSwitch('washtime')#工作时间 block
		btnstate = deviceSwitch("start")#启动

		if washinfo == "标准" and washstate == "暂停任务" and washtime == "" and btnstate == "启动":
			print "scuess,pause device scuess!"
			print "testcase ==> scuess"
			screenShot("./pic/pauseWashstandardScuess.png")
		else:
			print "【err】：pause device false,washinfo:%s washstate:%s washtime:%s btnstate:%s" %(washinfo,washstate,washtime,btnstate)
			print "testcase ==> false"
	else:
		print "【err】：device state is not running! btnstate:%s" %(btnstate)
		print "testcase ==> false"

#测试用例----关闭洗衣机
def testCase4switchClose4bolun():
	print "======== testCase4switchClose4bolun ========"
	if queryDeviceState() == 1:
		print "begin close cmd!"
		deviceSwitch("switch")
		time.sleep(5)
		if queryDeviceState() == 0:
			print "close device scuess!"
			print "testcase ==> scuess"
			screenShot("./pic/closeDeviceScuess.png")
		else:
			print "【err】：close device false!"
			print "testcase ==> false"
	else:
		print "【err】：device is not online! state:%s" %(queryDeviceState())
		print "testcase ==> false"

#主控函数
def main():
	browser.get("http://w.midea.com")

	if 0:
		#打印浏览器的useragent信息
		time.sleep(3)
		js = "return navigator.userAgent;"
		print "useragent:%s" %(browser.execute_script(js))
		
	#把配置中的cookie写入到w.midea.com域下
	cookies = getCookieFromConfig()
	addCookie2Domain(browser, cookies)
	
	#执行业务测试用例
	testCase4DeviceList()
	testCase4switchOpen4bolun()
	testCase4StandardRun4bolun()
	testCase4Babylock4bolun()
	testCase4StandardPause4bolun()
	testCase4switchClose4bolun()

if __name__ == '__main__':
	options = webdriver.ChromeOptions()
	options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
	#修改useragent
	options.add_argument('--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/600.1.3 (KHTML, like Gecko) Version/8.0 Mobile/12A4345d Safari/600.1.4')
	browser = webdriver.Chrome(chrome_options=options)
	
	#设置浏览器宽高 6+屏幕宽高
	browser.set_window_size(375, 650)
	time.sleep(2)

	url = "http://w.midea.com/littleswan/index.php/wxcontrol/devlist"
	main()
	#browser.quit()
