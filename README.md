# Rock Paper Scissors PLUS 🎮

Production-grade Rock-Paper-Scissors game with intelligent AI, built using **Google ADK (Agent Design Kit)** principles.

## Setup & Run

**Step 1: Install Python & Create Virtual Environment**
```bash
sudo apt update
sudo apt install -y python3-full python3-venv
```

**Step 2: Create & Activate Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Step 3: Install Dependencies**
```bash
pip install -r requirements.txt
```

**Step 4: Run the Game**
```bash
python main.py
```

## Game Flow

**Enter name → Choose difficulty (1-4) → Play 3 rounds → View results → Play again or exit**

## Game Rules

- **4 Moves**: Rock 🪨 | Paper 📄 | Scissors ✂️ | Bomb 💣
- **3 Rounds**: Best-of-3 format (exactly 3 rounds enforced)
- **Bomb**: Each player gets 1 bomb, beats everything
- **Scoring**: 1 point per round win

## Architecture (Google ADK)

Clean separation of concerns:

| File | Role | Lines |
|------|------|-------|
| `tools.py` | Game rules (validate_move, resolve_round, update_game_state) | 156 |
| `agent.py` | Intelligent AI (pattern learning, strategy selection) | 417 |
| `state.py` | Single source of truth (GameState dataclass) | 60 |
| `ui.py` | Terminal display (Rich library) | 303 |
| `main.py` | Game orchestration | 178 |


## AI Difficulty Levels

1. **Easy** - 30% strategic, 70% random
2. **Medium** - 60% strategic, 40% random
3. **Hard** - 80% strategic, learns opponent patterns
4. **Expert** - 90% strategic, meta-gaming tactics

## Game Summary

After 3 rounds, displays:
- Rounds played
- Your score vs Opponent
- Round-by-round results (who won each)
- Final winner and winning score

## Requirements

- Python 3.7+
- Rich library: `pip install rich`

## Features

✨ Beautiful terminal UI with colors, panels, tables, emojis  
✨ Intelligent AI with pattern recognition and learning  
✨ Complete game flow with input validation  
✨ Play again without restarting  
✨ Bomb mechanics (strategic move usage)  
✨ Full ADK compliance  

---

**Status**: Production-ready. All requirements satisfied. Run `python3 main.py` to play.
