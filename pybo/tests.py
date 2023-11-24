hi = 1
def change_name(a):
    a = 'how are you'
    return a
class MyClass:
    global hello
    hello = 'hello'
    hello = change_name(hello)


    def modify_global_var(self):
        global global_var
        global_var =10
        print(global_var)

    @classmethod
    def change_hello(cls):
        global hello, hi
        hello = 'me'
        hi = 2

obj = MyClass()
obj.modify_global_var()  # 출력: 15
MyClass.change_hello()
print(global_var,hello, hi)

if __name__=='__main__':
    print(hi)