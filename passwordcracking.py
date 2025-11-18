import hashlib
import time
from datetime import datetime
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn
from rich.table import Table

console = Console()
class PasswordCracker:
    def __init__(self, password_file, dictionary_file, output="cracked_passwords.txt"):
        """Initialize the password cracker with files"""
        self.password_hashes = self.load_password_file(password_file)
        self.dictionary = self.load_dictionary(dictionary_file)
        self.cracked = {}
        self.attempts = 0
        self.output_file = output
        
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
            console.print(f"[bold cyan] loaded {len(password_dict)} password hashes[/bold cyan]")
        except FileNotFoundError:
            console.print(f"Error: {filename} not found!", style= "bold red on yellow")
        return password_dict
    
    def load_dictionary(self, filename):
        """Load dictionary words from file"""
        words = []
        try:
            with open(filename, 'r') as f:
                words = [word.strip() for word in f if word.strip()]
            console.print(f"Loaded {len(words)} dictionary words", style="bold cyan")
        except FileNotFoundError:
            console.print(f"Error: {filename} not found!",style= "bold red on yellow")
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
                console.print(f"✓ Cracked User {user_id}: {candidate}", style="bold green")
                return True
        return False
    
    def attack_digits_only(self, max_length=8):
        """Strategy 1: Try digit-only passwords"""
        console.print("\nStrategy 1: Digit-Only Passwords", style ="bold yellow")
        start_time = time.time()
        
        # Common pass lengths
        for length in [4, 6, 8]:
            if length > max_length:
                break
            console.print(f"Trying {length}-digit passwords...", style="cyan")
            for num in range(10**length):
                candidate = str(num).zfill(length)
                self.check_password(candidate)
        
        # Date Passwords
        console.print("Trying date formats (YYYYMMDD)...", style="cyan")
        for year in range(1900, 2025):
            for month in range(1, 13):
                for day in range(1, 32):
                    candidate = f"{year}{month:02d}{day:02d}"
                    self.check_password(candidate)
        
        elapsed = time.time() - start_time
        console.print(f"Strategy 1 completed in {elapsed:.2f} seconds", style="green")
        console. print(f"Total cracked so far: {len(self.cracked)}", style="green")
    
    def attack_dictionary(self):
        """Strategy 2: Try dictionary words"""
        console.print("\nStrategy 2: Dictionary Words ", style="bold yellow")
        start_time = time.time()
        with Progress(SpinnerColumn(), BarColumn(), TextColumn("{task.description}"), TimeElapsedColumn()) as progress:
            task = progress.add_task("[white]Testing words...", total=len(self.dictionary))
        
        for word in self.dictionary:
            self.check_password(word)
            
            # Show progress every 1000 words
            if len(self.dictionary) > 1000 and self.attempts % 1000 == 0:
                console.print(f"Progress: {self.attempts} attempts, {len(self.cracked)} cracked", style="green")
        
        elapsed = time.time() - start_time
        console.print(f"Strategy 2 completed in {elapsed:.2f} seconds", style="green")
        console.print(f"Total cracked so far: {len(self.cracked)}", style="bold yellow")
    
    def attack_dictionary_plus_digits(self, max_digits=9999):
        """Strategy 3: Try dictionary words + digits"""
        console.print("\nStrategy 3: Dictionary + Digits", style="bold yellow")
        start_time = time.time()
        with Progress(SpinnerColumn(), BarColumn(), TimeElapsedColumn()) as progress:
            task = progress.add_task("[white]Testing combos...", total=len(self.dictionary))
        
        for i, word in enumerate(self.dictionary):
            # Try word + 1 to 4 digit numbers
            for num in range(max_digits + 1):
                self.check_password(f"{word}{num}")
            progress.update(task, advance=1)
            
            # Progress report
            if (i + 1) % 100 == 0:
                elapsed = time.time() - start_time
                console.print(f"Progress: {i+1}/{len(self.dictionary)} words, "
                      f"{len(self.cracked)} cracked, "
                      f"{elapsed:.1f}s elapsed", style="bold yellow")
        
        elapsed = time.time() - start_time
        console.print(f"Strategy 3 completed in {elapsed:.2f} seconds", style="green")
        console.print(f"Total cracked so far: {len(self.cracked)}", style="yellow")
    
    def save_results(self, output_file="cracked_passwords.txt"):
        """Save cracked passwords to file"""
        with open(output_file, 'w') as f:
            f.write("User ID | Password\n")
            f.write("-" * 40 + "\n")
            for user_id in sorted(self.cracked.keys(), key=int):
                f.write(f"{user_id} | {self.cracked[user_id]}\n")
        console.print(f"\nResults saved to {output_file}", style="bold magenta")
    
    def print_summary(self):
        """Print summary statistics"""
        total_users = len(self.password_hashes)
        cracked_count = len(self.cracked)
        success_rate = (cracked_count / total_users * 100) if total_users > 0 else 0

        table = Table(title="FINAL SUMMARY", title_style="bold green")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="bold")
        table.add_row("Total users: ", str(total_users))
        table.add_row("Passwords cracked:", str(cracked_count))
        table.add_row("Success rate", f"{success_rate:.2f}")
        table.add_row("Total attemps", f"{self.attempts}")
        console.print(table)
        
       # print("\n" + "=" * 50)
        #print("FINAL SUMMARY")
        #print("=" * 50)
        """print(f"Total users: {total_users}")
        print(f"Passwords cracked: {cracked_count}")
        print(f"Success rate: {success_rate:.2f}%")
        print(f"Total attempts: {self.attempts:,}")
        print("=" * 50)"""
    
    #def run_all_strategies(self):
      #  """Run all cracking strategies"""
        #print("Starting password cracking...")
        """print(f"Time started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        overall_start = time.time()
        
        # Run strategies in order
        self.attack_digits_only(max_length=8)
        self.attack_dictionary()
        
        
        self.attack_dictionary_plus_digits(max_digits=999)
        
        overall_elapsed = time.time() - overall_start
        
        print(f"\nTotal time: {overall_elapsed:.2f} seconds ({overall_elapsed/60:.2f} minutes)")
        
        self.print_summary()
        self.save_results()


# Main execution"""
#if __name__ == "__main__":
    # Initialize the password crack
    #crack = PasswordCracker("passwords.txt", "dictionary.txt")
    
    # verify first pass
""" print("\nVerifying User 1's password...")
    test_hash = crack.sha1_hash("123456")
    print(f"SHA-1 hash of '123456': {test_hash}")
    if '1' in crack.password_hashes:
        if crack.password_hashes['1'] == test_hash:
            print("✓ Verified: User 1's password is '123456'")
        else:
            print("✗ User 1's password is NOT '123456'")
    
    # run all
    crack.run_all_strategies()"""

