import itertools
import time

class LoginSystem:
    def __init__(self, correct_pin: str):
        self._correct_pin = correct_pin
        self.attempts = 0

    def try_login(self, pin: str) -> bool:
        self.attempts += 1
        return pin == self._correct_pin

def build_priority_groups():
    groups = {}

    groups["VERIFIED top 20 (real study data)"] = [
        "1234", "1111", "0000", "1212", "7777", 
        "1004", "2000", "4444", "2222", "6969", 
        "9999", "3333", "5555", "6666", "1122", 
        "1313", "8888", "4321", "2001", "1010",
    ]

    groups["EXTENDED known-common (documented, unranked)"] = [
        "2580", "0007", "0070", "1984", "1999", 
        "1919", "1972", "1122", "2020", "2021", 
        "2323", "6789", "2468", "1357", "1230", 
        "5201", "0101", "0808", "1231", "0704",
    ]

    groups["Repeated digits"] = [str(d) * 4 for d in range(10)]

    seqs = []
    for start in range(7):
        seqs.append("".join(str((start + i) % 10) for i in range(4)))
    for start in range(9, 2, -1):
        seqs.append("".join(str((start - i) % 10) for i in range(4)))
    groups["Sequential patterns"] = seqs

    groups["Likely years (1940-2015)"] = [str(y) for y in range(1940, 2016)]

    pairs = [f"{a}{a}{b}{b}" for a in range(10) for b in range(10) if a != b]
    groups["Repeated-pair patterns (XYXY)"] = pairs

    return groups

def build_least_likely_group():
    return [
        "8557", "9047", "8438", "0439", "9539", 
        "8196", "7063", "6093", "6827", "7394", 
        "0859", "8957", "9480", "6793", "8398", 
        "0738", "7637", "6835", "9629", "8093", 
        "8068",
    ]

def build_full_search_space():
    return [f"{i:04d}" for i in range(10000)]

def crack_pin(login: LoginSystem):
    tried = set()
    start_time = time.time()

    priority_groups = build_priority_groups()

    for group_name, pins in priority_groups.items():
        print(f"\nTrying: {group_name} ({len(pins)} candidates)")
        for pin in pins:
            if pin in tried:
                continue
            tried.add(pin)
            if login.try_login(pin):
                return report_success(pin, login, start_time, group_name)
            if login.attempts % 10 == 0 or login.attempts <= 5:
                print(
                    f"  attempt {login.attempts:>5} | tried {pin} | elapsed {time.time()-start_time:.2f}s"
                )

    print(f"\nFull brute-force (0000-9999)")
    for pin in build_full_search_space():
        if pin in tried:
            continue
        tried.add(pin)
        if login.try_login(pin):
            return report_success(pin, login, start_time, "Full brute-force")
        if login.attempts % 500 == 0:
            print(f"  attempt {login.attempts:>5} | tried {pin} | elapsed {time.time()-start_time:.2f}s"
            )

    print("\nPIN not found.")
    return None

def report_success(pin, login, start_time, group_name):
    elapsed = time.time() - start_time
    print(f"\n{'='*50}")
    print(f"PIN cracked: {pin}")
    print(f"In group:    {group_name}")
    print(f"Attempts:    {login.attempts}")
    print(f"Time:       {elapsed:.4f} seconds")
    print(f"{'='*50}")
    return pin

if __name__ == "__main__":
    SECRET_PIN = "1948"

    system = LoginSystem(correct_pin=SECRET_PIN)
    cracked = crack_pin(system)

    least_likely = build_least_likely_group()
    if cracked in least_likely:
        rank_from_bottom = least_likely.index(cracked) + 1
        print(
            f"\nNote: {cracked} is one of the VERIFIED least-used real-world "
            f"PINs (bottom {rank_from_bottom} of the least common)."
        )