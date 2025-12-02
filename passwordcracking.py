import hashlib
import itertools
from datetime import datetime

class PasswordCracker:
    def __init__(self, password_file, dictionary_file):
        self.hashes = self.load_hashes(password_file)
        self.words = self.load_words(dictionary_file)
        self.cracked = {}
        self.attempts = 0
        self.start_time = datetime.now()
        self.hash_to_uid = {v: k for k, v in self.hashes.items()}
        
        print(f"Loaded {len(self.words)} words, targeting {len(self.hashes)} passwords\n")
    
    def load_hashes(self, filename):
        d = {}
        with open(filename) as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) == 2:
                    d[parts[0]] = parts[1].lower()
        return d
    
    def load_words(self, filename):
        with open(filename) as f:
            return [w.strip().lower() for w in f if w.strip()]
    
    def sha1(self, s):
        return hashlib.sha1(s.encode()).hexdigest()
    
    def check(self, cand):
        self.attempts += 1
        h = self.sha1(cand)
        
        if h in self.hash_to_uid:
            uid = self.hash_to_uid[h]
            if uid not in self.cracked:
                print(f"✓✓✓ User {uid}: '{cand}' ✓✓✓")
                self.cracked[uid] = cand
                return True
        return False
    
    def quick_wins(self):
        """Get the easy ones first"""
        print("[Quick] Single words + word+1-4 digits + pure numbers 1-6 digits...")
        
        # Single words
        for w in self.words:
            if self.check(w):
                if len(self.cracked) == len(self.hashes):
                    return True
        
        # Word + 1-4 digits
        for w in self.words:
            for d in range(10000):
                if self.check(w + str(d)):
                    if len(self.cracked) == len(self.hashes):
                        return True
        
        # Pure numbers 1-6 digits
        for d in range(1000000):
            if self.check(str(d)):
                if len(self.cracked) == len(self.hashes):
                    return True
            if d % 200000 == 0:
                print(f"  Numbers: {d:,}/1,000,000", end='\r')
        
        print(f"\n  Cracked: {len(self.cracked)}/{len(self.hashes)}\n")
        return len(self.cracked) == len(self.hashes)
    
    def word_5_6_digits_top_words(self):
        """Word + 5-6 digits but only top 500 most common words"""
        print("[Focused] Word + 5-6 digits (TOP 500 words only)...")
        print("  This checks ~500M combinations instead of 5B")
        
        for i, w in enumerate(self.words[:500]):
            for d in range(10000, 1000000):
                if self.check(w + str(d)):
                    if len(self.cracked) == len(self.hashes):
                        return True
            
            if i % 25 == 0:
                progress = i / 500 * 100
                elapsed = (datetime.now() - self.start_time).total_seconds()
                rate = self.attempts / elapsed if elapsed > 0 else 0
                remaining = (500 - i) * 990000 / rate / 60 if rate > 0 else 0
                print(f"  Word {i}/500 ({progress:.1f}%) | Rate: {rate:,.0f}/s | ETA: {remaining:.1f}min | Cracked: {len(self.cracked)}/{len(self.hashes)}")
        
        print(f"  Cracked: {len(self.cracked)}/{len(self.hashes)}\n")
        return len(self.cracked) == len(self.hashes)
    
    def digits_5_6_plus_word(self):
        """5-6 digits + word (top 500 words)"""
        print("[Focused] 5-6 digits + word (TOP 500 words)...")
        
        for i, w in enumerate(self.words[:500]):
            for d in range(10000, 1000000):
                if self.check(str(d) + w):
                    if len(self.cracked) == len(self.hashes):
                        return True
            
            if i % 25 == 0:
                progress = i / 500 * 100
                print(f"  Word {i}/500 ({progress:.1f}%) | Cracked: {len(self.cracked)}/{len(self.hashes)}")
        
        print(f"  Cracked: {len(self.cracked)}/{len(self.hashes)}\n")
        return len(self.cracked) == len(self.hashes)
    
    def three_words_aggressive(self):
        """Three words - larger search"""
        print("[Focus] Three words (length ≤ 6, top 600 words)...")
        short = [w for w in self.words if len(w) <= 6][:600]
        total = len(short) ** 3
        
        print(f"  Total combinations: {total:,}")
        
        for i, combo in enumerate(itertools.product(short, repeat=3)):
            if self.check("".join(combo)):
                if len(self.cracked) == len(self.hashes):
                    return True
            
            if i % 500000 == 0:
                progress = i / total * 100
                elapsed = (datetime.now() - self.start_time).total_seconds()
                rate = i / elapsed if elapsed > 0 else 0
                eta = (total - i) / rate / 60 if rate > 0 else 0
                print(f"  {i//1000000}M/{total//1000000}M ({progress:.1f}%) | ETA: {eta:.1f}min | Cracked: {len(self.cracked)}/{len(self.hashes)}")
        
        print(f"  Cracked: {len(self.cracked)}/{len(self.hashes)}\n")
        return len(self.cracked) == len(self.hashes)
    
    def two_words_plus_digits_aggressive(self):
        """Two words + 1-4 digits (larger search)"""
        print("[Focus] Two words + 1-4 digits (top 500 words)...")
        
        subset = [w for w in self.words if len(w) <= 6][:500]
        total = len(subset) ** 2 * 10000
        count = 0
        
        print(f"  Total combinations: {total:,}")
        
        for w1, w2 in itertools.product(subset, repeat=2):
            for d in range(10000):
                if self.check(w1 + w2 + str(d)):
                    if len(self.cracked) == len(self.hashes):
                        return True
                count += 1
                
                if count % 1000000 == 0:
                    progress = count / total * 100
                    print(f"  {count//1000000}M/{total//1000000}M ({progress:.1f}%) | Cracked: {len(self.cracked)}/{len(self.hashes)}")
        
        print(f"  Cracked: {len(self.cracked)}/{len(self.hashes)}\n")
        return len(self.cracked) == len(self.hashes)
    
    def four_words_aggressive(self):
        """Four words (bigger search)"""
        print("[Focus] Four words (length ≤ 4, top 200 words)...")
        tiny = [w for w in self.words if len(w) <= 4][:200]
        total = len(tiny) ** 4
        
        print(f"  Total combinations: {total:,}")
        
        for i, combo in enumerate(itertools.product(tiny, repeat=4)):
            if self.check("".join(combo)):
                if len(self.cracked) == len(self.hashes):
                    return True
            
            if i % 500000 == 0:
                progress = i / total * 100
                elapsed = (datetime.now() - self.start_time).total_seconds()
                rate = i / elapsed if elapsed > 0 else 0
                eta = (total - i) / rate / 60 if rate > 0 else 0
                print(f"  {i//1000000}M/{total//1000000}M ({progress:.1f}%) | ETA: {eta:.1f}min | Cracked: {len(self.cracked)}/{len(self.hashes)}")
        
        print(f"  Cracked: {len(self.cracked)}/{len(self.hashes)}\n")
        return len(self.cracked) == len(self.hashes)
    
    def pure_numbers_extended(self):
        """Pure numbers 7-10 digits (sampled)"""
        print("[Sampled] Pure numbers 7-10 digits...")
        
        # 7-8 digits: every 5th
        print("  7-8 digits (every 5th)...")
        for d in range(1000000, 100000000, 5):
            if self.check(str(d)):
                if len(self.cracked) == len(self.hashes):
                    return True
            if d % 10000000 == 0:
                print(f"  {d:,}", end='\r')
        
        # 9-10 digits: every 100th
        print("\n  9-10 digits (every 100th)...")
        for d in range(100000000, 10000000000, 100):
            if self.check(str(d)):
                if len(self.cracked) == len(self.hashes):
                    return True
            if d % 500000000 == 0:
                print(f"  {d:,}", end='\r')
        
        print(f"\n  Cracked: {len(self.cracked)}/{len(self.hashes)}\n")
        return len(self.cracked) == len(self.hashes)
    
    def run(self):
        print(f"Starting FAST-FINISH cracker at {datetime.now().strftime('%H:%M:%S')}\n")
        print("Strategy: Skip the 5B combination phase, focus on likely patterns\n")
        
        strategies = [
            ("Quick wins", self.quick_wins),
            ("Three words", self.three_words_aggressive),
            ("Four words", self.four_words_aggressive),
            ("Two words + digits", self.two_words_plus_digits_aggressive),
            ("Word + 5-6 digits (top 500)", self.word_5_6_digits_top_words),
            ("5-6 digits + word (top 500)", self.digits_5_6_plus_word),
            ("Pure numbers 7-10 (sampled)", self.pure_numbers_extended),
        ]
        
        for name, func in strategies:
            print(f"{'='*70}")
            print(f"{name}")
            print(f"{'='*70}")
            
            if func():
                print("\n🎉 ALL 20 PASSWORDS CRACKED! 🎉")
                break
        
        self.finish()
    
    def finish(self):
        elapsed = (datetime.now() - self.start_time).total_seconds()
        print("\n" + "="*70)
        print("FINAL RESULTS")
        print("="*70)
        print(f"Cracked: {len(self.cracked)}/{len(self.hashes)} passwords")
        print(f"Time: {elapsed/60:.1f} minutes")
        print(f"Total attempts: {self.attempts:,}")
        print(f"Rate: {self.attempts/elapsed:,.0f} attempts/sec")
        
        if len(self.cracked) < len(self.hashes):
            missing = sorted([int(u) for u in self.hashes if u not in self.cracked])
            print(f"\nMissing {len(missing)}: {missing}")
            print("\nThese likely require:")
            print("  - Exhaustive word+5-6 digits (ALL 5000 words)")
            print("  - Word + 7-10 digits")
            print("  - More than 4 words")
        
        print("\nCRACKED:")
        for uid in sorted(self.cracked.keys(), key=int):
            print(f"  User {uid:>3}: {self.cracked[uid]}")

if __name__ == "__main__":
    cracker = PasswordCracker("passwords.txt", "dictionary.txt")
    cracker.run()
