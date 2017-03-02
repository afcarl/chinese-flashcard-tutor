import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "turk_chinese.settings")
django.setup()

from chinese_tutor.models import FlashCard
from chinese_tutor.models import UserAttempt

flash_cards = set()

with open("/Users/cmaclell/Desktop/chinese-learning/DS213 - Chinese Character Learning.txt", 'r', encoding="utf-16") as fin:
    count = 0
    first = True
    last_student = None
    for line in fin:

        if first:
            first = False
            continue
        if line == "":
            continue

        stu = line.split('\t')[1]
        if stu != last_student:
            last_student = stu

        anon_stu = line.split('\t')[1]
        stimulus = line.split('\t')[5]
        problem_type = line.split('\t')[6]
        response = line.split('\t')[4]

        if problem_type != "english":
            continue

        if stimulus == "" or problem_type == "" or response == "":
            continue

        fc = (stimulus, response, problem_type)

        if fc not in flash_cards:
            count += 1
            flash_cards.add((stimulus, response, problem_type))

        if count >= 10:
            break


for stimulus, response, problem_type in flash_cards:
    fc = FlashCard(stimulus=stimulus, response=response,
                   response_type=problem_type)
    fc.save()
    print(stimulus, problem_type, response)
