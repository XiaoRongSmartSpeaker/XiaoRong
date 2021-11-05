from pypinyin import pinyin
import re


keyword = [
	['打電話給', '撥電話', '打給'],#call related 
	['行事曆', '提醒我', '要幹嘛', '有什麼事']
]

dec_pinyin = ['líng','yī','èr','sān','sì','wǔ','liù','qī','bā','jiǔ']

def text2Function(command):
	command_found = -1
	for word_list in keyword:
		for word in word_list:
			if(word in command):
				# print('THERE IS KEYWORD IN THE STR')
				return keyword.index(word_list)
	return len(keyword) #the last function 問答

def isPhoneNumber(str):
	return re.match(r'\d(-\d)*', str)

def call_by_name(name):
	print('你要打給聯絡人：' , name)
	return

def call_by_number(number):
	print('你要打給號碼：' , number)
	return

def call(input_str):
	for word in keyword[which_function]:
		location = input_str.find(word)
		if(location!=-1):
			target = input_str[location+len(word):]
			break
		else :
			continue
	if(isPhoneNumber(target)):
		call_by_number(target)
		return
	target_pinyin = pinyin(target)
	call_by_name(target_pinyin)
	return



def calender(input_str):
	print('B')

def ask(input_str):
	print('C')


function_list = [call, calender, ask]

test_str = '幫我打給HsuanYu'

which_function = text2Function(test_str)
function_list[which_function](test_str)