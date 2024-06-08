from hanspell import spell_checker
from hanspell.constants import CheckResult
import requests
import os


text="밥을머것다.기분이조타"

print("교정 전:"+text)

spelled_text = spell_checker.check(text)
print("교정 후:"+spelled_text.checked)
spelled_text.as_dict()
spelled_text

for key, value in spelled_text.words.items():
    if value == 0:
        # print("맞춤법 검사 통과:",key)
        pass
    elif value ==1:
        print("맞춤법 오류:",key)
    elif value ==2:
        print("띄어쓰기 오류:",key)
    elif value ==3:
        print("표준어 의심:",key)
    elif value ==4:
        print("통계적 오류 의심:",key)
