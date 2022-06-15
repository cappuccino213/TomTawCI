"""
@File : multiple_thread.py
@Date : 2022/6/15 14:12
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""
# 重写多线程类，含返回值

import threading


class MultipleThread(threading.Thread):
	def __init__(self, func, args=()):
		super().__init__()
		self.func = func
		self.args = args
		self.result = []

	def run(self):
		self.result = self.func(*self.args)

	def get_result(self):
		try:
			return self.result
		except Exception:
			return None


if __name__ == "__main__":
	"""sample
	def is_even(value):
		if value % 2 == 0:
			return True
		else:
			return False
	result = []
	threads = []
	for i in range(10):
		t = MultipleThread(is_even, args=(i,))
		t.start()
		threads.append(t)
	for t in threads:
		t.join()  # 一定执行join,等待子进程执行结束，主进程再往下执行
		result.append(t.get_result())
	print(result)
	"""
	pass
