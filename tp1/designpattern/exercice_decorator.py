import time


def log_time(func):
    def inner_log_time():
        start = time.time_ns()
        func()
        end = time.time_ns()
        print(end - start)
    return inner_log_time

def super_log_time(func):
    def inner_super_log_time():
        print('super log time')
        func()
    return inner_super_log_time

@super_log_time
@log_time
def quack():
    print('quack')
    time.sleep(1)
    print('quack')


#quack = super_log_time(log_time(quack))

if __name__ == '__main__':
    print(type(quack))
    # quack
    # quack
    # 1
    quack()