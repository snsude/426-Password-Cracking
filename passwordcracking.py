import hashlib
import time
from datetime import datetime

class PasswordCracker:
    def __init__(self, password_file, dictionary_file):
        """Initialize the password cracker with files"""
        self.password_hashes = self.load_password_file(password_file)
        self.dictionary = self.load_dictionary(dictionary_file)
        self.cracked = {}
        self.attempts = 0
        
    def load_password_file(self, filename):
        """Load password hashes from file"""
        password_dict = {}
        try:
            with open(filename, 'r') as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) == 2:
                        user_id, hash_value = parts
                        password_dict[user_id] = hash_value.lower()
            print(f"Loaded {len(password_dict)} password hashes")
        except FileNotFoundError:
            print(f"Error: {filename} not found!")
        return password_dict
    
    def load_dictionary(self, filename):
        """Load dictionary words from file"""
        words = []
        try:
            with open(filename, 'r') as f:
                words = [word.strip().lower() for word in f if word.strip()]
            print(f"Loaded {len(words)} dictionary words")
        except FileNotFoundError:
            print(f"Error: {filename} not found!")
        return words
    
    def sha1_hash(self, password):
        """Calculate SHA-1 hash of a password"""
        return hashlib.sha1(password.encode()).hexdigest()
    
    def check_password(self, candidate):
        """Check if candidate matches any hash"""
        self.attempts += 1
        hash_val = self.sha1_hash(candidate)
        
        for user_id, stored_hash in self.password_hashes.items():
            if user_id not in self.cracked and hash_val == stored_hash:
                self.cracked[user_id] = candidate
                print(f"✓ Cracked User {user_id}: {candidate}")
                return True
        return False
    
    def attack_digits_only(self, max_length=8):
        """Strategy 1: Try digit-only passwords"""
        print("\nStrategy 1: Digit-Only Passwords")
        start_time = time.time()
        
        # Common pass lengths
        for length in [4, 6, 8]:
            if length > max_length:
                break
            print(f"Trying {length}-digit passwords...")
            for num in range(10**length):
                candidate = str(num).zfill(length)
                self.check_password(candidate)
        
        # Date Passwords
        print("Trying date formats (YYYYMMDD)...")
        for year in range(1900, 2025):
            for month in range(1, 13):
                for day in range(1, 32):
                    candidate = f"{year}{month:02d}{day:02d}"
                    self.check_password(candidate)
        
        elapsed = time.time() - start_time
        print(f"Strategy 1 completed in {elapsed:.2f} seconds")
        print(f"Total cracked so far: {len(self.cracked)}")
    
    def attack_dictionary(self):
        """Strategy 2: Try dictionary words"""
        print("\nStrategy 2: Dictionary Words ")
        start_time = time.time()
        
        for word in self.dictionary:
            self.check_password(word)
            
            # Show progress every 1000 words
            if len(self.dictionary) > 1000 and self.attempts % 1000 == 0:
                print(f"Progress: {self.attempts} attempts, {len(self.cracked)} cracked")
        
        elapsed = time.time() - start_time
        print(f"Strategy 2 completed in {elapsed:.2f} seconds")
        print(f"Total cracked so far: {len(self.cracked)}")
    
    def attack_dictionary_plus_digits(self, max_digits=9999):
        """Strategy 3: Try dictionary words + digits"""
        print("\nStrategy 3: Dictionary + Digits")
        print(f"This will try each word with 0-{max_digits}")
        start_time = time.time()
        
        for i, word in enumerate(self.dictionary):
            # Try word + 1 to 4 digit numbers
            for num in range(max_digits + 1):
                candidate = f"{word}{num}"
                self.check_password(candidate)
            
            # Progress report
            if (i + 1) % 100 == 0:
                elapsed = time.time() - start_time
                print(f"Progress: {i+1}/{len(self.dictionary)} words, "
                      f"{len(self.cracked)} cracked, "
                      f"{elapsed:.1f}s elapsed")
        
        elapsed = time.time() - start_time
        print(f"Strategy 3 completed in {elapsed:.2f} seconds")
        print(f"Total cracked so far: {len(self.cracked)}")
    
    def save_results(self, output_file="cracked_passwords.txt"):
        """Save cracked passwords to file"""
        with open(output_file, 'w') as f:
            f.write("User ID | Password\n")
            f.write("-" * 40 + "\n")
            for user_id in sorted(self.cracked.keys(), key=int):
                f.write(f"{user_id} | {self.cracked[user_id]}\n")
        print(f"\nResults saved to {output_file}")
    
    def print_summary(self):
        """Print summary statistics"""
        total_users = len(self.password_hashes)
        cracked_count = len(self.cracked)
        success_rate = (cracked_count / total_users * 100) if total_users > 0 else 0
        
        print("\n" + "=" * 50)
        print("FINAL SUMMARY")
        print("=" * 50)
        print(f"Total users: {total_users}")
        print(f"Passwords cracked: {cracked_count}")
        print(f"Success rate: {success_rate:.2f}%")
        print(f"Total attempts: {self.attempts:,}")
        print("=" * 50)
    
    def run_all_strategies(self):
        """Run all cracking strategies"""
        print("Starting password cracking...")
        print(f"Time started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        overall_start = time.time()
        
        # Run strategies in order
        self.attack_digits_only(max_length=8)
        self.attack_dictionary()
        
        
        self.attack_dictionary_plus_digits(max_digits=999)
        
        overall_elapsed = time.time() - overall_start
        
        print(f"\nTotal time: {overall_elapsed:.2f} seconds ({overall_elapsed/60:.2f} minutes)")
        
        self.print_summary()
        self.save_results()


# Main execution
if __name__ == "__main__":
    # Initialize the password crack
    crack = PasswordCracker("passwords.txt", "dictionary.txt")
    
    # verify first pass
    print("\nVerifying User 1's password...")
    test_hash = crack.sha1_hash("123456")
    print(f"SHA-1 hash of '123456': {test_hash}")
    if '1' in crack.password_hashes:
        if crack.password_hashes['1'] == test_hash:
            print("✓ Verified: User 1's password is '123456'")
        else:
            print("✗ User 1's password is NOT '123456'")
    
    # run all
    crack.run_all_strategies()

