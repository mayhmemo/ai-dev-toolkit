from .base import Command, console
import typer
from rich.prompt import Confirm
from rich.panel import Panel
from pydantic_ai import Agent
from pydantic import BaseModel
from ai_dev_toolkit.utils.misc.utils import get_operational_system
import os

class CliResultType(BaseModel):
    command: str

system_prompt = f"""
You are a CLI command assistant.
Given a user request, you will provide a command to execute on the CLI.
The command should be a valid command that can be executed on the CLI.
Always provide the full command, including any necessary flags or arguments.
this command should be a single line command.
This command must run correctly on the system {get_operational_system()}.
"""

class TerminalBuilderCommand(Command):
    def __init__(self):
        super().__init__(
            name="cli-command",
            help="Build and execute terminal commands using AI"
            
        )
        self.agent = Agent('groq:llama3-8b-8192', result_type=CliResultType, system_prompt=system_prompt)
    
    def execute(self, request: str):
        try:
            result = self.agent.run_sync(request)
            command = result.data.command
            
            console.print(Panel(
                f"[bold blue]Generated Command:[/]\n[green]{command}[/]",
                title="AI Command Builder",
                border_style="blue"
            ))
            
            if Confirm.ask("Do you want to execute this command?"):
                console.print("\n[bold yellow]Executing command...[/]")
                os.system(command)
        except Exception as e:
            console.print(f"[bold red]Error:[/] {str(e)}") 

