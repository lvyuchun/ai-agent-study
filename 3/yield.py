import sys
gen = (i**2 for i in range(1000) if i%2 == 0)
list = list(gen)
print(sys.getsizeof(gen))
print(sys.getsizeof(list))
def num():
    print("1")
    yield 1
    print("2")
    yield 2   
def read_line(file_name):
    with open(file_name) as f:
        for line in f:
            print(line.strip())
            yield line.strip()
    
for line in read_line("yield.txt"):
    pass


