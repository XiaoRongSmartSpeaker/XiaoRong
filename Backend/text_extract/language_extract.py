language_dict = {"中文":"zh-TW", "英文":"en", "法文":"fr"}
def target_language(inputSTR):
	if('翻' in inputSTR):
		fromLanguage = inputSTR[:inputSTR.index('翻')]
		fromLanguage.lstrip()
		toLanguage = inputSTR[inputSTR.index('翻')+1:]
		toLanguage.lstrip()
		if(len(fromLanguage)==0 or len(toLanguage)==0 or (fromLanguage not in language_dict) or (toLanguage not in language_dict)):
			return [None, None]
		else:
			return (language_dict[fromLanguage], language_dict[toLanguage])
	else:
		return [None, None]