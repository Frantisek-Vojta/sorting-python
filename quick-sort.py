import random
import time

def quick_sort(data):
    if len(data) <= 1:
        return data
    pivot = data[0]
    left = [x for x in data if x < pivot]
    middle = [x for x in data if x == pivot]
    right = [x for x in data if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

def generate_numbers(count, low=-10000, high=10000):
    return [random.randint(low, high) for _ in range(count)]

print("kolik cisel seradit:")
print("1 - 10")
print("2 - 5000")
print("3 - vlastni pocet")
choice = input("volba: ").strip()

if choice == "1":
    count = 10
elif choice == "2":
    count = 5000
elif choice == "3":
    count = int(input("pocet cisel:"))
else:
    print("neplatne cislo")
    count = 10

numbers = generate_numbers(count)

start = time.perf_counter()
numbers = quick_sort(numbers)
end = time.perf_counter()

print("cisla:", numbers)
print(f"Serazeno {count} čísel za {end - start:.6f} s")