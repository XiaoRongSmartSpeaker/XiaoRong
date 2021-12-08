import re

def place_target(full_input_str):
	input_str = full_input_str
	place = None
	place_re = re.compile(r'(查詢(.*)時間|(.*)時區)')
	place_obj = place_re.match(input_str)
	if(place_obj):
		if('時間' in input_str):
			place = place_obj.group(2)
		elif('時區' in input_str):
			place = place_obj.group(3)
	return place
