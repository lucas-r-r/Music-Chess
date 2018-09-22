
class The_class():
    def __init__(self):
        print("I've init")
    def __str__(self):
        return "I'm the class"

class Another_class():
    def __str__(self):
        return "I'm another class"

dictio = {'1': The_class,
        '2': Another_class,
        '3': 'caca'

        }

inst_The_class = dictio['1']()
print(inst_The_class)
