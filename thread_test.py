import threading
import time
def two_job():
	print('thread %s is running...' % threading.current_thread().name)
	for i in range(5):
		print("我是第二個程式：", i)
		time.sleep(0.5)
def three_job():
	print("i am the three_job")
two= threading.Thread(target = two_job)
three=threading.Thread(target=three_job)
two.start()
three.start()
print(threading.active_count())
for i in range(2):
	print("我是主要程式碼", i)
	time.sleep(1)
two.join()
three.join()
print("Done.")