from dataclasses import dataclass

@dataclass
class Function:
  name: str
  value: object
  args: list[str]