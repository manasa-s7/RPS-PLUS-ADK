
"""
GameState - Single Source of Truth for Game Data

Why a dedicated state module?
1. Centralized state definition
2. Type-safe with dataclass
3. Easy to serialize/persist
4. Clear schema for all state
5. Immutable structure (only mutated via tools)

Mutation Flow:
    GameState created → passed to functions → modified via tools → returned

No state hidden in globals or function parameters beyond what's needed.
All game data flows through this dataclass.
"""

from dataclasses import dataclass, field


@dataclass
class GameState:
    """
    Complete game state definition.
    
    This is the single source of truth. Everything the game needs to know
    is here. Nothing is hidden in module globals or closures.
    
    Fields:
        round (int): Current round (1-3). Incremented by update_game_state()
        user_score (int): Points earned by player. Incremented by update_game_state()
        bot_score (int): Points earned by bot. Incremented by update_game_state()
        user_bomb_used (bool): Whether player has used bomb. Set by main.py
        bot_bomb_used (bool): Whether bot has used bomb. Set by main.py
    
    Invariants:
    - round is always 1-3 (game ends after round 3 becomes 4)
    - user_score and bot_score are always 0-3
    - Bomb flags are boolean
    
    Example State Lifecycle:
        Start:     round=1, user_score=0, bot_score=0, bombs_unused
        Round 1:   Player wins → user_score=1, round=2
        Round 2:   Draw → scores unchanged, round=3
        Round 3:   Bot wins → bot_score=1, round=4 → game ends
    
    Why Dataclass?
    - Type-safe (mypy compatible)
    - Serializable (can save/load)
    - Immutable contract (only mutate via tools)
    - Clear schema (self-documenting)
    - Easy to add fields later (game_history, timestamps, etc.)
    """
    round: int = 1              # Current round number
    user_score: int = 0         # Player's points (0-3)
    bot_score: int = 0          # Bot's points (0-3)
    user_bomb_used: bool = False  # Has player used special move?
    bot_bomb_used: bool = False   # Has bot used special move?
