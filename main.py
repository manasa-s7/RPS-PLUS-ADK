"""
Rock Paper Scissors PLUS - ADK Agent Implementation

This module orchestrates the game following Google ADK principles:
- Tools (tools.py) handle game logic with clear contracts
- Agent (agent.py) makes intelligent decisions using tools
- State (state.py) maintains single source of truth
- UI (ui.py) handles presentation
"""

import random
import time
from state import GameState
from agent import AIAgent
from tools import validate_move, resolve_round, update_game_state
from ui import (
    banner, show_rules, show_score, show_round_header, 
    show_moves, show_round_result, show_final_result, 
    show_invalid_move, show_move_prompt, clear_screen,
    show_game_statistics
)
from config import VALID_MOVES, EMOJIS
from rich.console import Console

console = Console()


def get_player_name():
    """Prompt player to enter their name."""
    clear_screen()
    console.print("\n[bold cyan]👤 WELCOME TO ROCK PAPER SCISSORS PLUS! 👤[/bold cyan]\n", justify="center")
    
    while True:
        console.print("[bold yellow]Enter your name:[/bold yellow]", end=" ")
        name = input().strip()
        if name:
            return name
        else:
            console.print("[bold red]Please enter a valid name![/bold red]")


def select_difficulty():
    """Let player select difficulty level."""
    clear_screen()
    console.print("\n[bold cyan]🎮 SELECT DIFFICULTY[/bold cyan]\n", justify="center")
    console.print("[bold green]1. Easy[/bold green] - Opponent is forgiving")
    console.print("[bold yellow]2. Medium[/bold yellow] - Balanced challenge")
    console.print("[bold red]3. Hard[/bold red] - Smart Opponent with patterns")
    console.print("[bold magenta]4. Expert[/bold magenta] - Maximum intelligence\n")
    
    while True:
        choice = input("Enter choice (1-4): ").strip()
        if choice == "1":
            return "easy"
        elif choice == "2":
            return "medium"
        elif choice == "3":
            return "hard"
        elif choice == "4":
            return "expert"
        else:
            console.print("[bold red]Invalid choice! Try again.[/bold red]")


def main():
    # Get player name
    player_name = get_player_name()
    
    # Select difficulty
    difficulty = select_difficulty()
    
    state = GameState()
    agent = AIAgent(difficulty=difficulty)
    
    banner()
    console.print(f"[bold magenta]👋 Welcome, {player_name}![/bold magenta]\n", justify="center")
    console.print(f"[bold magenta]🤖 Opponent Difficulty: {difficulty.upper()}[/bold magenta]\n", justify="center")
    time.sleep(1)
    
    show_rules()
    input("Press [ENTER] to start the game...")
    
    # Track per-round outcomes for summary
    round_outcomes = []

    while state.round <= 3:
        clear_screen()
        show_score(state, player_name)
        show_round_header(state.round)
        show_move_prompt()
        
        user_input = input(">>> ").strip().lower()
        val = validate_move(user_input, state.user_bomb_used)

        if not val["valid"]:
            show_invalid_move()
            time.sleep(2)
            # Record invalid round outcome, then advance round
            round_outcomes.append({
                "round": state.round,
                "result": "Invalid move - no winner"
            })
            state.round += 1
            continue

        user_move = val["move"]
        user_emoji = EMOJIS.get(user_move, "")
        
        if user_move == "bomb":
            state.user_bomb_used = True

        # AI makes intelligent decision
        bot_move = agent.get_ai_move(state.user_bomb_used, state.bot_bomb_used)
        
        # Fallback: ensure bot doesn't use bomb twice
        if bot_move == "bomb" and state.bot_bomb_used:
            bot_move = random.choice(["rock", "paper", "scissors"])
        elif bot_move == "bomb":
            state.bot_bomb_used = True
        
        bot_emoji = EMOJIS.get(bot_move, "")

        time.sleep(0.5)
        show_moves(user_move, bot_move, user_emoji, bot_emoji, player_name)
        time.sleep(1.5)
        
        # Capture current round before state advances
        current_round = state.round
        winner = resolve_round(user_move, bot_move)
        
        # Record outcome label
        if winner == "user":
            outcome_label = f"{player_name}"
        elif winner == "bot":
            outcome_label = "Opponent"
        else:
            outcome_label = "Draw"
        round_outcomes.append({
            "round": current_round,
            "result": outcome_label
        })

        state = update_game_state(state, winner)
        
        # Update AI history for learning
        agent.update_history(user_move, bot_move)
        
        show_round_result(winner, user_move, bot_move, player_name)
        
        input("Press [ENTER] for next round...")

    clear_screen()
    show_final_result(state, player_name)
    
    # Show beautiful statistics dashboard with round-by-round results
    show_game_statistics(player_name, agent, state, round_outcomes)
    
    # Ask to play again
    console.print("\n[bold yellow]Would you like to play again?[/bold yellow]", justify="center")
    console.print("[cyan]1. Yes - Play Again[/cyan]", justify="center")
    console.print("[cyan]2. No - Exit[/cyan]\n", justify="center")
    
    while True:
        choice = input("Enter choice (1-2): ").strip()
        if choice == "1":
            console.print("\n[bold green]🎮 Starting new game...[/bold green]\n", justify="center")
            time.sleep(1)
            main()  # Restart the game
            break
        elif choice == "2":
            console.print("\n[bold cyan]👋 Thanks for playing! Goodbye![/bold cyan]\n", justify="center")
            break
        else:
            console.print("[bold red]Invalid choice! Please enter 1 or 2.[/bold red]", justify="center")


if __name__ == "__main__":
    main()
