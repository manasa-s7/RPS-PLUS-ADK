
from rich.console import Console
from rich.panel import Panel
from rich.layout import Layout
from rich.table import Table
from rich.text import Text
from rich.align import Align
from rich.style import Style
from rich.live import Live
import time

console = Console()

def clear_screen():
    """Clear the terminal screen"""
    console.clear()

def banner():
    """Display an animated, beautiful banner"""
    clear_screen()
    banner_text = Text()
    banner_text.append("🎮 ", style="bold magenta")
    banner_text.append("ROCK PAPER SCISSORS", style="bold cyan")
    banner_text.append(" PLUS ", style="bold yellow")
    banner_text.append("💣", style="bold red")
    
    panel = Panel(
        Align.center(banner_text),
        style="bold cyan",
        border_style="bold magenta",
        padding=(1, 2),
        expand=False
    )
    console.print(Align.center(panel))
    console.print()

def show_rules():
    """Display game rules in a beautiful panel"""
    rules_text = Text()
    rules_text.append("📋 GAME RULES\n\n", style="bold yellow")
    rules_text.append("🎯 Best of 3 rounds\n", style="cyan")
    rules_text.append("💣 Each player gets ONE bomb\n", style="red")
    rules_text.append("⚡ Bomb beats all moves\n", style="magenta")
    rules_text.append("🔄 Invalid moves waste a round\n", style="yellow")
    rules_text.append("\n📌 Moves: rock • paper • scissors • bomb", style="green")
    
    panel = Panel(
        rules_text,
        style="green",
        border_style="bold green",
        padding=(1, 2)
    )
    console.print(Align.center(panel))
    console.print()

def show_score(state, player_name="YOU"):
    """Display scores in a beautiful table format"""
    table = Table(
        title="📊 CURRENT SCORE",
        show_header=True,
        header_style="bold magenta",
        border_style="cyan",
        padding=(0, 2),
        expand=False
    )
    
    table.add_column("Player", style="bold cyan", justify="center")
    table.add_column("Score", style="bold yellow", justify="center")
    table.add_column("Bomb Used", style="bold red", justify="center")
    
    user_bomb = "✓ Yes" if state.user_bomb_used else "✗ No"
    bot_bomb = "✓ Yes" if state.bot_bomb_used else "✗ No"
    
    table.add_row(f"👤 {player_name.upper()}", str(state.user_score), user_bomb)
    table.add_row("🤖 BOT", str(state.bot_score), bot_bomb)
    
    console.print(Align.center(table))
    console.print()

def show_round_header(round_num):
    """Display round header with animation"""
    console.print()
    round_text = Text()
    round_text.append("⚔️  ", style="bold red")
    round_text.append(f"ROUND {round_num}", style="bold yellow")
    round_text.append("  ⚔️", style="bold red")
    
    panel = Panel(
        Align.center(round_text),
        style="bold yellow",
        border_style="red",
        padding=(1, 2)
    )
    console.print(Align.center(panel))
    console.print()

def show_moves(user_move, bot_move, user_emoji, bot_emoji, player_name="YOU"):
    """Display user and bot moves side by side"""
    table = Table(
        show_header=False,
        border_style="cyan",
        padding=(1, 2),
        expand=False
    )
    
    table.add_column("Player", style="bold cyan", justify="center", width=15)
    table.add_column("Move", style="bold yellow", justify="center", width=15)
    
    user_text = Text(f"{user_emoji} {user_move.upper()}", style="bold green")
    bot_text = Text(f"{bot_emoji} {bot_move.upper()}", style="bold blue")
    
    table.add_row(f"👤 {player_name.upper()}", user_text)
    table.add_row("🤖 BOT", bot_text)
    
    console.print(Align.center(table))
    console.print()

def show_round_result(winner, user_move, bot_move, player_name="YOU"):
    """Display round result with animation"""
    result_text = Text()
    
    if winner == "user":
        result_text.append("✨ ", style="bold yellow")
        result_text.append(f"{player_name.upper()} WINS THIS ROUND!", style="bold green")
        result_text.append(" ✨", style="bold yellow")
        style = "green"
    elif winner == "bot":
        result_text.append("💀 ", style="bold red")
        result_text.append("BOT WINS THIS ROUND!", style="bold red")
        result_text.append(" 💀", style="bold red")
        style = "red"
    else:
        result_text.append("🤝 ", style="bold magenta")
        result_text.append("IT'S A DRAW!", style="bold magenta")
        result_text.append(" 🤝", style="bold magenta")
        style = "magenta"
    
    panel = Panel(
        Align.center(result_text),
        style=f"bold {style}",
        border_style=style,
        padding=(1, 2)
    )
    console.print(Align.center(panel))
    console.print()

def show_final_result(state, player_name="YOU"):
    """Display final game result with celebration"""
    console.print()
    console.print("═" * 60)
    
    # Final scores
    table = Table(
        title="🏆 FINAL SCORES 🏆",
        show_header=True,
        header_style="bold gold1",
        border_style="gold1",
        padding=(1, 2),
        expand=False
    )
    
    table.add_column("Player", style="bold cyan", justify="center")
    table.add_column("Final Score", style="bold yellow", justify="center")
    
    table.add_row(f"👤 {player_name.upper()}", str(state.user_score))
    table.add_row("🤖 BOT", str(state.bot_score))
    
    console.print(Align.center(table))
    console.print()
    
    # Result
    result_text = Text()
    if state.user_score > state.bot_score:
        result_text.append("🎉 ", style="bold green")
        result_text.append(f"CONGRATULATIONS, {player_name.upper()}! YOU ARE THE CHAMPION! 🎉", style="bold green")
        style = "green"
    elif state.user_score < state.bot_score:
        result_text.append("🤖 ", style="bold red")
        result_text.append(f"THE BOT DOMINATES, {player_name.upper()}! BETTER LUCK NEXT TIME! 🤖", style="bold red")
        style = "red"
    else:
        result_text.append("⚖️ ", style="bold yellow")
        result_text.append(f"AN HONORABLE DRAW, {player_name.upper()}! WELL PLAYED! ⚖️", style="bold yellow")
        style = "yellow"
    
    panel = Panel(
        Align.center(result_text),
        style=f"bold {style}",
        border_style=style,
        padding=(1, 2),
        expand=False
    )
    console.print(Align.center(panel))
    console.print("═" * 60)
    console.print()

def show_invalid_move():
    """Display invalid move message"""
    warning_text = Text()
    warning_text.append("⚠️  ", style="bold red")
    warning_text.append("INVALID MOVE! ROUND WASTED! ⚠️", style="bold red")
    
    panel = Panel(
        Align.center(warning_text),
        style="bold red",
        border_style="red",
        padding=(1, 2)
    )
    console.print(Align.center(panel))
    console.print()

def show_move_prompt():
    """Display move selection prompt"""
    prompt_text = Text()
    prompt_text.append("\n💡 ", style="bold cyan")
    prompt_text.append("Enter your move: ", style="bold white")
    
    moves_text = Text()
    moves_text.append("[", style="yellow")
    moves_text.append("🪨 rock", style="cyan")
    moves_text.append(" | ", style="yellow")
    moves_text.append("📄 paper", style="cyan")
    moves_text.append(" | ", style="yellow")
    moves_text.append("✂️ scissors", style="cyan")
    moves_text.append(" | ", style="yellow")
    moves_text.append("💣 bomb", style="red")
    moves_text.append("]", style="yellow")
    
    console.print(Align.center(prompt_text))
    console.print(Align.center(moves_text))
    console.print()


def show_game_statistics(player_name, agent, state, rounds):
    """Display simple game statistics"""
    # Keep this summary minimal and clear per user request
    
    console.print("\n")
    console.print("[bold cyan]═" * 50 + "[/bold cyan]", justify="center")
    console.print("[bold yellow]📊 GAME SUMMARY[/bold yellow]\n", justify="center")
    
    # Rounds played
    console.print(f"[cyan]Rounds Played:[/cyan] [bold]{len(agent.opponent_history)}[/bold]", justify="center")
    console.print()
    
    # Individual scores
    console.print(f"[cyan]{player_name.upper()} Score:[/cyan] [bold green]{state.user_score}[/bold green]", justify="center")
    console.print(f"[cyan]OPPONENT Score:[/cyan] [bold red]{state.bot_score}[/bold red]", justify="center")
    console.print()

    # Round-by-round results
    if rounds:
        console.print("[bold cyan]Round Results:[/bold cyan]", justify="center")
        for entry in sorted(rounds, key=lambda r: r.get("round", 0)):
            console.print(f"[white]Round {entry['round']}[/white]: [bold]{entry['result']}[/bold]", justify="center")
        console.print()
    
    # Winner announcement
    if state.user_score > state.bot_score:
        console.print(f"[bold green]🏆 WINNER: {player_name.upper()} 🏆[/bold green]", justify="center")
        console.print(f"[green]Winning Score: {state.user_score}[/green]", justify="center")
    elif state.bot_score > state.user_score:
        console.print(f"[bold red]🏆 WINNER: OPPONENT 🏆[/bold red]", justify="center")
        console.print(f"[red]Winning Score: {state.bot_score}[/red]", justify="center")
    else:
        console.print(f"[bold yellow]🤝 IT'S A TIE! 🤝[/bold yellow]", justify="center")
        console.print(f"[yellow]Both scored {state.user_score} point(s)[/yellow]", justify="center")
    console.print()

    console.print()
    console.print("[bold cyan]═" * 50 + "[/bold cyan]", justify="center")

