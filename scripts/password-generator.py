import random

words = open('scripts/words.txt').read().splitlines()
possible_words = [x for x in words if len(x) > 3 and len(x)<7 ]

for i in range(155):
    print(f"{random.choice(possible_words).capitalize()}{random.choice(possible_words).capitalize()}{random.randint(1,9)}")