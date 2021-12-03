import re
import number_tran


def target_volume(input_str):
	percent = re.compile(r'((\d+)|((一百)|(二|三|四|五|六|七|八|九)?((十?(一|二|兩|三|四|五|六|七|八|九))|十)))(趴|%)?')
	target_obj = percent.search(input_str)
	if('零' in input_str):
		target_num = 0 
	elif('百' in input_str or '千' in input_str):
		target_num = 100
	elif(target_obj):
		target_str = target_obj.group()
		if('趴' in target_str):
			target_str = target_str.replace('趴', '')
		elif('%' in target_str):
			target_str = target_str.replace('%', '')
		target_num = number_tran._trans(target_str)
		if('百' in input_str or target_num>100):
			target_num = 100
	else:
		return [None]
	if(input_str[0] == '負' or input_str[0] == '-'):
		target_num *= -1
	return [target_num]
