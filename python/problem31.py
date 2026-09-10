import itertools
import time

password = "blrss"

digits = "ahrsblk0123456789"

found = False
attempts = 0

start = time.time()

for length in range(1, len(password) + 1):

    for combination in itertools.product(digits, repeat=length):
        candidate = ''.join(combination)
        attempts += 1

        print(f"Trying: {candidate}")

        if candidate == password:
            elapsed = time.time() - start

            print("\nPassword confirmeed!")
            print("Password:", candidate)
            print("Attempts:", attempts)
            print(f"Time: {elapsed:.4f} seconds")

            found = True
            break

    if found:
        break

if not found:
    print("Password not found")