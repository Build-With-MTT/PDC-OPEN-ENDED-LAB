# cores.py - Part A(c): CPU cores and the best number of workers  (RUN THIS ON UBUNTU)
import os
import psutil

physical = psutil.cpu_count(logical=False)
logical = os.cpu_count()
print("Physical cores (psutil.cpu_count(logical=False)):", physical)
print("Logical cores  (os.cpu_count())                 :", logical)
print("Largest sensible number of workers              :", logical,
      "(more workers than logical cores only wait for each other)")
