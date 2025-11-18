
from __future__ import annotations
import hashlib
import bcrypt
from passwordcracking import PasswordCracker

import argparse #pass arguments
import csv #read csv or write save
from typing import List, Dict, Tuple, Optional
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
import sys
from pathlib import Path


try:
  from rich.panel import Panel
  from rich.table import Table
  from rich import print as rprint
  from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn
  from rich.prompt import Prompt, Confirm
  from rich.console import Console
  from rich.text import Text
  RICH_AVAILABLE = True #check if rich libary is available
  console = Console()


except ImportError:
  RICH_AVAILABLE =False
  console =None
  #SpinnerColumn = None
  #TimeElapsedColumn = None
  print("NB: 'rich library is not available please use pip to install; on Windows use python -m pip install  rich")
  print("Using the basic console output")
  

def display_banner():
  banner = """███████╗ █████╗ ███╗   ███╗███████╗██████╗ 
██╔════╝██╔══██╗████╗ ████║██╔════╝██╔══██╗
█████╗  ███████║██╔████╔██║█████╗  ██████╔╝
██╔══╝  ██╔══██║██║╚██╔╝██║██╔══╝  ██╔══██╗
███████╗██║  ██║██║ ╚═╝ ██║███████╗██║  ██║
╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝╚═╝  ╚═╝"""
  if RICH_AVAILABLE:
    console.print(Panel(Text(banner, style = "bold cyan"), title ="[bold red] EducationHash Verification - Class Project[/bold red]" ,
    subtitle = "[yellow] Authorized learning only [/yellow] ",
    border_style="bright_blue"))
  else:
    print(banner)
    print("="*70)
    print("Educational Password Tool - Authorized Learning Only")
  print("="*70)

"""def show_header():
  console.print(Panel.fit("[bold cyan] Hash Verification - Class Project[/bold cyan]\nPassword hash cracking tool for class project. It shows the importance of using stronger password",
                          title ="HASH  Verifier",
                          subtitle="Secure .Fast. Clean"))
#show_header()"""
def build_parser():
    parser = argparse.ArgumentParser(
        description="Educational SHA‑1 Password Cracker"
    )

    parser.add_argument("--passwords", required=True,
                        help="Path to file containing user SHA‑1 hashes")
    parser.add_argument("--dictionary", required=True,
                        help="Path to dictionary wordlist")
    parser.add_argument("--output", default="cracked_passwords.txt",
                        help="File where cracked passwords will be saved")

    # Strategy options
    parser.add_argument("--digits-only", action="store_true",
                        help="Run digit‑only attack")
    parser.add_argument("--dictionary-only", action="store_true",
                        help="Run dictionary‑only attack")
    parser.add_argument("--dict-plus-digits", action="store_true",
                        help="Run dictionary + digits attack")

    parser.add_argument("--all", action="store_true",
                        help="Run all strategies")

    parser.add_argument("--max-digits", type=int, default=999,
                        help="Max digits to append for dictionary+digits attack")

    return parser

def main():
  if RICH_AVAILABLE:
    console.clear()
  display_banner()

  parse =build_parser()
  args = parse.parse_args()
  crack_password = PasswordCracker(args.passwords, args.dictionary, args.output)

  #determining what to run
  if args.all:
    crack_password.attack_digits_only()
    crack_password.attack_dictionary()
    crack_password.attack_dictionary_plus_digits(args.max_digits)
  else:
    if args.digits_only:
      crack_password.attack_digits_only()
    if args.dictionary_only:
      crack_password.attack_dictionary()
    if args.dict_plus_digits:
      crack_password.attack_dictionary_plus_digits(args.max_digits)

  crack_password.print_summary()
  crack_password.save_results()

if __name__ =="__main__":
  main()
