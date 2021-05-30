import multiprocessing
import time


class ProcessClass:
    @staticmethod
    def run(target, args: tuple):
        p = multiprocessing.Process(target=target, args=args)
        p.start()

    @staticmethod
    def wait_process_quit():
        while len(multiprocessing.active_children()) != 0:
            time.sleep(1)
            print("=== main wait===")


def worker(arg1, arg2):
    n = 5
    while n > 0:
        time.sleep(1)
        print(arg1, arg2)
        n -= 1


if __name__ == "__main__":
    ProcessClass.run(worker, (1, 2))
    ProcessClass.run(worker, (3, 4))
    ProcessClass.wait_process_quit()
