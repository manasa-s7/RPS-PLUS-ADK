
"""
ADK Tools - Pure Game Logic Functions

These tools implement game rules as independent, testable functions.
Each tool:
1. Takes structured input
2. Applies game logic
3. Returns structured output
4. Does NOT mutate external state (except where explicitly intended)

This separation enables:
- Independent testing
- Clear responsibility boundaries
- Easy rule modifications
- Audit trails for all decisions
"""

import random
from typing import Dict
from config import VALID_MOVES


def validate_move(move: str, bomb_used: bool) -> Dict:
    """
    TOOL: Validate user move against game rules.
    
    Responsibility: Enforce move legality
    - Check move is in VALID_MOVES (rock, paper, scissors, bomb)
    - Check bomb hasn't been used already
    
    Args:
        move (str): User's move input (case-insensitive)
        bomb_used (bool): Whether this player has used bomb before
    
    Returns:
        Dict with structure:
        {
            "valid": bool,      # Move is legal
            "move": str,        # Normalized move (if valid)
            "reason": str       # Error message (if invalid)
        }
    
    Contract:
    - Input: move (any string), bomb_used (bool)
    - Output: Structured dict with guaranteed fields
    - Side effects: None (pure function)
    
    Examples:
        validate_move("rock", False) → {"valid": True, "move": "rock"}
        validate_move("bomb", True)  → {"valid": False, "reason": "Bomb already used"}
        validate_move("invalid", False) → {"valid": False, "reason": "Invalid move"}
    """
    move = move.lower().strip()
    if move not in VALID_MOVES:
        return {"valid": False, "reason": "Invalid move"}
    if move == "bomb" and bomb_used:
        return {"valid": False, "reason": "Bomb already used"}
    return {"valid": True, "move": move}


def resolve_round(user_move: str, bot_move: str) -> str:
    """
    TOOL: Determine round winner using rock-paper-scissors rules.
    
    Responsibility: Apply game logic
    - Rock beats scissors
    - Scissors beats paper
    - Paper beats rock
    - Bomb beats everything
    - Same move = draw
    
    Args:
        user_move (str): Player's move (must be valid)
        bot_move (str): Bot's move (must be valid)
    
    Returns:
        str: One of ["user", "bot", "draw"]
    
    Contract:
    - Input: Two valid moves
    - Output: Guaranteed winner string
    - Side effects: None (pure function)
    - Can be tested independently
    
    Examples:
        resolve_round("rock", "scissors") → "user"
        resolve_round("bomb", "rock")     → "user"
        resolve_round("rock", "rock")     → "draw"
        resolve_round("paper", "scissors") → "bot"
    """
    # Same move = automatic draw
    if user_move == bot_move:
        return "draw"
    
    # Both bombs = draw (special case)
    if user_move == "bomb" and bot_move == "bomb":
        return "draw"
    
    # Bomb beats everything
    if user_move == "bomb":
        return "user"
    if bot_move == "bomb":
        return "bot"
    
    # Standard rock-paper-scissors rules
    rules = {
        "rock": "scissors",      # rock beats scissors
        "scissors": "paper",     # scissors beats paper
        "paper": "rock"          # paper beats rock
    }
    
    return "user" if rules[user_move] == bot_move else "bot"


def update_game_state(state, winner: str):
    """
    TOOL: Update game state after a round.
    
    Responsibility: Mutate game state
    - Increment winner's score
    - Advance to next round
    
    Args:
        state (GameState): Current game state (mutable)
        winner (str): Round result ("user", "bot", "draw")
    
    Returns:
        GameState: Updated state (same object, modified)
    
    Contract:
    - Input: Valid GameState and winner string
    - Output: Modified GameState
    - Side effects: Increments score, advances round
    - All state mutations go through this function (single point of mutation)
    
    Examples:
        state.user_score = 0, state.round = 1
        → update_game_state(state, "user")
        → state.user_score = 1, state.round = 2
    
    Why a separate tool?
    - Centralizes all state mutations
    - Makes it easy to audit state changes
    - Easy to add side effects (logging, analytics, etc.)
    - Prevents state from being mutated in multiple places
    """
    if winner == "user":
        state.user_score += 1
    elif winner == "bot":
        state.bot_score += 1
    # draw: no points to either player
    
    state.round += 1
    return state
