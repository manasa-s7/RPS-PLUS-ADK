"""
AIAgent - Intelligent Decision Making Component

The AIAgent uses tools (not implements them) to make smart decisions.

Key Distinction:
- TOOLS (tools.py): Enforce rules, return facts (immutable)
- AGENT (this file): Learns patterns, makes decisions (intelligent)

Agent Design:
1. Updates history after each round
2. Analyzes opponent patterns
3. Detects repeating sequences
4. Makes decisions based on difficulty
5. Uses validated tools for rule-checking

The agent demonstrates learning and adaptation without
implementing the actual game rules (which tools handle).
"""

import random
from typing import Dict, List
from collections import defaultdict
from config import VALID_MOVES


class AIAgent:
    """
    Intelligent AI Agent for Rock-Paper-Scissors-Plus.
    
    Uses strategy patterns, learning, and game theory.
    Does NOT implement game rules (tools.py does).
    Focuses on intelligent decision-making.
    
    Difficulty Levels:
    - easy: 30% pattern-based, 70% random
    - medium: 60% pattern-based, 40% random
    - hard: 80% pattern-based, 20% random
    - expert: 90% pattern-based, 10% random + meta-gaming
    """
    
    def __init__(self, difficulty: str = "hard"):
        """
        Initialize agent with difficulty level.
        
        Args:
            difficulty (str): One of ["easy", "medium", "hard", "expert"]
        """
        self.difficulty = difficulty
        self.move_history = []          # Bot's past moves
        self.opponent_history = []      # Opponent's past moves
        self.move_patterns = defaultdict(list)  # Pattern tracking
        self.last_moves = []            # Recent moves for pattern detection
        self.pattern_length = 3
        
    def update_history(self, player_move: str, bot_move: str):
        """
        Record moves after each round (learning mechanism).
        
        Args:
            player_move (str): What player did
            bot_move (str): What bot did
        
        This enables:
        - Pattern detection
        - Move frequency analysis
        - Adaptation over time
        """
        self.opponent_history.append(player_move)
        self.move_history.append(bot_move)
        self.last_moves.append(player_move)
        
        # Keep recent history for pattern analysis
        if len(self.last_moves) > 10:
            self.last_moves.pop(0)
    
    def get_counter_move(self, move: str) -> str:
        """
        Get move that beats the given move.
        
        Helper for strategy: if opponent plays X, return counter to X.
        
        Args:
            move (str): Opponent's move
        
        Returns:
            str: Move that beats input
        """
        counters = {
            "rock": "paper",
            "paper": "scissors",
            "scissors": "rock",
            "bomb": "bomb"
        }
        return counters.get(move, "rock")
    
    def analyze_patterns(self) -> Dict[str, float]:
        """
        Analyze opponent's move distribution.
        
        Returns:
            Dict: Frequency of each move (0.0 to 1.0)
        
        Example output:
        {"rock": 0.4, "paper": 0.3, "scissors": 0.3}
        """
        if not self.opponent_history:
            return {"rock": 0.33, "paper": 0.33, "scissors": 0.33}
        
        move_counts = {"rock": 0, "paper": 0, "scissors": 0}
        for move in self.opponent_history:
            if move in move_counts:
                move_counts[move] += 1
        
        total = sum(move_counts.values())
        return {
            move: count / total for move, count in move_counts.items()
        }
    
    def detect_repeating_pattern(self) -> str:
        """
        Detect if opponent repeats a move sequence.
        
        Example: If opponent plays rock-paper-scissors-rock-paper-scissors,
        detect the 3-move pattern and predict next move.
        
        Returns:
            str: Predicted counter to next move, or None
        """
        if len(self.last_moves) >= self.pattern_length:
            pattern = tuple(self.last_moves[-self.pattern_length:])
            pattern_index = 0
            
            # Count how many times pattern repeats in history
            for i in range(len(self.opponent_history) - self.pattern_length):
                if (tuple(self.opponent_history[i:i+self.pattern_length]) == pattern):
                    pattern_index += 1
            
            # If pattern repeats 2+ times, it's predictable
            if pattern_index >= 2:
                next_index = (self.pattern_length) % 3
                if next_index < len(self.last_moves):
                    return self.get_counter_move(self.last_moves[next_index])
        
        return None
    
    def get_ai_move(self, player_bomb_used: bool, bot_bomb_used: bool) -> str:
        """
        Make intelligent move decision based on difficulty.
        
        Decision Tree:
        1. Try pattern detection (if works, use 60% of time)
        2. Analyze most-used opponent move
        3. Decide whether to use bomb (if available)
        4. Apply difficulty-based strategy
        5. Return move
        
        Args:
            player_bomb_used (bool): Can we still use bomb?
            bot_bomb_used (bool): Have we used bomb already?
        
        Returns:
            str: Chosen move (rock, paper, scissors, or bomb)
        
        Difficulty Behavior:
        - easy: Mostly random with hints of counters
        - medium: Balance between pattern learning and randomness
        - hard: Aggressive pattern learning
        - expert: Meta-gaming and prediction
        """
        
        # Strategy 1: Pattern Detection (works on repeaters)
        pattern_move = self.detect_repeating_pattern()
        if pattern_move and random.random() < 0.6:
            return pattern_move
        
        # Strategy 2: Counter Most-Used Move
        patterns = self.analyze_patterns()
        most_used_move = max(patterns, key=patterns.get)
        counter = self.get_counter_move(most_used_move)
        
        # Strategy 3: Bomb Usage (strategic timing)
        if not bot_bomb_used and len(self.opponent_history) >= 2:
            # Use bomb if we're losing
            bot_wins = sum(1 for i, move in enumerate(self.move_history) 
                          if self._would_win(move, self.opponent_history[i]))
            
            if len(self.opponent_history) >= 2 and bot_wins < len(self.opponent_history) // 2:
                if random.random() < 0.4:
                    return "bomb"
        
        # Strategy 4: Difficulty-based decision
        if self.difficulty == "easy":
            # Easy: mostly random, sometimes smart
            if random.random() < 0.3:
                return counter
            return random.choice(["rock", "paper", "scissors"])
        
        elif self.difficulty == "medium":
            # Medium: balance between learning and random
            if random.random() < 0.6:
                return counter
            else:
                return random.choice(["rock", "paper", "scissors"])
        
        elif self.difficulty == "hard":
            # Hard: aggressive learning strategy
            if random.random() < 0.8:
                if random.random() < 0.6:
                    return counter
                else:
                    # Secondary: use weak move to bait next response
                    weak_to_counter = self.get_counter_move(counter)
                    return weak_to_counter
            return random.choice(["rock", "paper", "scissors"])
        
        elif self.difficulty == "expert":
            # Expert: maximum intelligence with meta-gaming
            if random.random() < 0.9:
                if random.random() < 0.7:
                    return counter
                else:
                    # Meta-gaming: beat the counter they'll use
                    meta_counter = self.get_counter_move(counter)
                    return self.get_counter_move(meta_counter)
            return random.choice(["rock", "paper", "scissors"])
        
        # Fallback
        return counter
    
    def _would_win(self, bot_move: str, player_move: str) -> bool:
        """
        Check if bot move would win against player move.
        
        Helper for bomb-timing strategy.
        
        Args:
            bot_move (str): What bot played
            player_move (str): What player played
        
        Returns:
            bool: Whether bot would win
        """
        if bot_move == player_move:
            return False
        if bot_move == "bomb":
            return True
        if player_move == "bomb":
            return False
        
        rules = {
            "rock": "scissors",
            "scissors": "paper",
            "paper": "rock"
        }
        return rules[bot_move] == player_move
    
    def reset(self):
        """Reset agent for new game."""
        self.move_history = []
        self.opponent_history = []
        self.move_patterns = defaultdict(list)
        self.last_moves = []

    """
    Intelligent AI agent for Rock-Paper-Scissors-Plus
    Uses strategy patterns, learning, and game theory
    """
    
    def __init__(self, difficulty: str = "hard"):
        self.difficulty = difficulty
        self.move_history = []  # Bot's move history
        self.opponent_history = []  # Player's move history
        self.move_patterns = defaultdict(list)  # Player pattern tracking
        self.last_moves = []  # Recent moves for pattern analysis
        self.pattern_length = 3
        
    def update_history(self, player_move: str, bot_move: str):
        """Track moves for pattern learning"""
        self.opponent_history.append(player_move)
        self.move_history.append(bot_move)
        self.last_moves.append(player_move)
        
        # Keep only recent moves for analysis
        if len(self.last_moves) > 10:
            self.last_moves.pop(0)
    
    def get_counter_move(self, move: str) -> str:
        """Get the move that beats the given move"""
        counters = {
            "rock": "paper",
            "paper": "scissors",
            "scissors": "rock",
            "bomb": "bomb"
        }
        return counters.get(move, "rock")
    
    def analyze_patterns(self) -> Dict[str, float]:
        """Analyze player's move frequency and patterns"""
        if not self.opponent_history:
            return {"rock": 0.33, "paper": 0.33, "scissors": 0.33}
        
        move_counts = {"rock": 0, "paper": 0, "scissors": 0}
        for move in self.opponent_history:
            if move in move_counts:
                move_counts[move] += 1
        
        total = sum(move_counts.values())
        return {
            move: count / total for move, count in move_counts.items()
        }
    
    def detect_repeating_pattern(self) -> str:
        """Detect if player is repeating a pattern"""
        if len(self.last_moves) >= self.pattern_length:
            pattern = tuple(self.last_moves[-self.pattern_length:])
            pattern_index = 0
            
            # Look for repeating pattern in history
            for i in range(len(self.opponent_history) - self.pattern_length):
                if (tuple(self.opponent_history[i:i+self.pattern_length]) == pattern):
                    pattern_index += 1
            
            # If pattern repeats, predict next move
            if pattern_index >= 2:
                next_index = (self.pattern_length) % 3
                if next_index < len(self.last_moves):
                    return self.get_counter_move(self.last_moves[next_index])
        
        return None
    
    def get_ai_move(self, player_bomb_used: bool, bot_bomb_used: bool) -> str:
        """
        Intelligent decision-making based on difficulty and game state
        """
        
        # Strategy 1: Pattern Detection
        pattern_move = self.detect_repeating_pattern()
        if pattern_move and random.random() < 0.6:
            return pattern_move
        
        # Strategy 2: Counter Most Used Move
        patterns = self.analyze_patterns()
        most_used_move = max(patterns, key=patterns.get)
        counter = self.get_counter_move(most_used_move)
        
        # Strategy 3: Bomb Usage
        if not bot_bomb_used and len(self.opponent_history) >= 2:
            # Use bomb if we're losing or in critical moment
            bot_wins = sum(1 for i, move in enumerate(self.move_history) 
                          if self._would_win(move, self.opponent_history[i]))
            
            if len(self.opponent_history) >= 2 and bot_wins < len(self.opponent_history) // 2:
                if random.random() < 0.4:
                    return "bomb"
        
        # Strategy 4: Difficulty-based decision
        if self.difficulty == "easy":
            # Easy: mostly random with some counter
            if random.random() < 0.3:
                return counter
            return random.choice(["rock", "paper", "scissors"])
        
        elif self.difficulty == "medium":
            # Medium: balance between pattern and random
            if random.random() < 0.6:
                return counter
            else:
                return random.choice(["rock", "paper", "scissors"])
        
        elif self.difficulty == "hard":
            # Hard: aggressive strategy, heavy use of patterns
            if random.random() < 0.8:
                if random.random() < 0.6:
                    return counter
                else:
                    # Secondary strategy: use weak move to bait
                    weak_to_counter = self.get_counter_move(counter)
                    return weak_to_counter
            return random.choice(["rock", "paper", "scissors"])
        
        elif self.difficulty == "expert":
            # Expert: maximum intelligence
            if random.random() < 0.9:
                if random.random() < 0.7:
                    return counter
                else:
                    # Psychological play: use moves that beat the counter
                    meta_counter = self.get_counter_move(counter)
                    return self.get_counter_move(meta_counter)
            return random.choice(["rock", "paper", "scissors"])
        
        return counter
    
    def _would_win(self, bot_move: str, player_move: str) -> bool:
        """Check if bot move would win"""
        if bot_move == player_move:
            return False
        if bot_move == "bomb":
            return True
        if player_move == "bomb":
            return False
        
        rules = {
            "rock": "scissors",
            "scissors": "paper",
            "paper": "rock"
        }
        return rules[bot_move] == player_move
    
    def reset(self):
        """Reset for new game"""
        self.move_history = []
        self.opponent_history = []
        self.move_patterns = defaultdict(list)
        self.last_moves = []
