from .base import Command, console

class HelloCommand(Command):
    def __init__(self):
        super().__init__(
            name="hello",
            help="A friendly greeting command"
        )
    
    def execute(self, name: str = "World"):
        console.print(f"[bold blue]Hello, {name}! 👋[/]") 