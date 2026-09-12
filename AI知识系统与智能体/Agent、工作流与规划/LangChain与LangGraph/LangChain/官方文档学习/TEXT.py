from dataclasses import dataclass


@dataclass
class a:
    b:int = 1

print(a(b=2).b)