
from __future__ import annotations
import hashlib
import bcrypt

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
  Panel = None
  TextColumn = None
  Text = None
  Confirm = None
  Table = None
  Prompt = None
  BarColumn = None
  SpinnerColumn = None
  TimeElapsedColumn = None
  print("NB: 'rich library is not available please use pip to install; on Windows use python -m pip install  rich")
  print("Using the basic console output")
  class console_basics:
    def print(self, text, **kwargs):
      import re
      text_clean = re.sub(r'\[/?[^\]]*\]','',str(text)) #remove something related to  rich formating
      print(text_clean)
    def clear(self):
      import os
      #cls for windows and clear for linux
      os.system('cls' if os.name =='nt' else 'clear')
  console = console_basics
try:
  import pyfiglet
  PYFIGLET_AVAILABLE = False
except:
  PYFIGLET_AVAILABLE = False
@dataclass
class HashEntry:
  """Representing a hash entry with optional username and metadata"""
  hash_value : str  #The actual hash value
  user: Optional[str] = None #use name default to Nome
  hash_type: Optional[str] = None #Algorithm used default to none

  def __str__(self):
    #if the user exist, show the user name and hash value
    if self.user:
      return "{} : {}".format(self.user, self.hash_value)
    #Otherwise return the hash value
    return self.hash_value
HASH_ALGORITHMS = {
  "1": {"name": "MD5", "func": hashlib.md5},
  "2": {"name" :"SHA-1", "func": hashlib.sha1 },
  "3": {"name": "SHA-224", 'func': hashlib.sha224},
  "4": {"name": "SHA-256", "func": hashlib.sha256},
  "5" : {"name": "SHA-512", "func": hashlib.sha512}
}


def display_Warnings():
  banner =pyfiglet.figlet_format("Hash Demo", font="block")
 
  if PYFIGLET_AVAILABLE:
    banner =pyfiglet.figlet_format("Hash Demo", font="block")
    print("hello word")
  else:
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

def show_header():
  console.print(Panel.fit("[bold cyan] Hash Verification - Class Project[/bold cyan]\nPassword hash cracking tool for class project. It shows the importance of using stronger password",
                          title ="HASH  Verifier",
                          subtitle="Secure .Fast. Clean"))
#show_header()

def main():
  console.clear()
  display_Warnings()


main()
