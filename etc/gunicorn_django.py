import multiprocessing

bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count()*2+1
#django project root dir
chdir = "/home/box/web/ask"