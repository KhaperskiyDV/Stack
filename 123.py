class TestClass:
    def __init__(self, is_true):
        self.is_true = is_true


    def say_true_or_false(self):
        if self.is_true:
            return 'true'
        else:
            return 'false'
        
        

true_answer = TestClass(True)
false_answer = TestClass(False)


print(true_answer.say_true_or_false())
print(false_answer.say_true_or_false())