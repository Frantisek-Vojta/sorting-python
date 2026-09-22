import random
import time

def bubble_sort(data):
    n = len(data)
    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]
                swapped = True
        if not swapped:
            break

def generate_numbers(count, low=-1000, high=1000):
    return [random.randint(low, high) for _ in range(count)]

print("Kolik cisel seradit:")
print("1 - 10")
print("2 - 5000")
print("3 - vlastni pocet")
choice = input("Volba: ").strip()

if choice == "1":
    count = 10
elif choice == "2":
    count = 5000
elif choice == "3":
    count = int(input("pocet cisel:"))
else:
    print("neplatne cislo")

numbers = generate_numbers(count)

start = time.perf_counter()
bubble_sort(numbers)
end = time.perf_counter()

print(f"Seřazeno {count} čísel za {end - start:.6f} s")