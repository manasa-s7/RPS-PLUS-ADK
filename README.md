# Rock Paper Scissors PLUS ADK – AI Game Referee

Production-grade Rock-Paper-Scissors game with intelligent AI, built using **Google ADK (Agent Design Kit)** principles.

## Setup & Run

### 🪟 **Windows**

**Step 1: Install Python**
- Download from [python.org](https://www.python.org/downloads/)
- Run installer and check "Add Python to PATH"

**Step 2: Create & Activate Virtual Environment**
```cmd
python -m venv venv
venv\Scripts\activate
```

**Step 3: Install Dependencies**
```cmd
pip install -r requirements.txt
```

**Step 4: Run the Game**
```cmd
python main.py
```

---

### 🐧 **Ubuntu/Linux**

**Step 1: Install Python & venv**
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
python3 main.py
```

---

## Design Details (Submission)

### State Model
**GameState** dataclass holds the complete game state:
- `round` (1-3): Current round number
- `user_score`, `bot_score` (0-3): Points earned
- `user_bomb_used`, `bot_bomb_used` (bool): Bomb availability

No hidden state. All game data flows explicitly through this structure.

### Agent/Tool Design
**ADK Separation**:
- **Tools** (tools.py): Pure game logic - validate moves, resolve rounds, update state
- **Agent** (agent.py): Intelligent decisions - learns patterns, adapts to difficulty
- **Main** (main.py): Orchestrates flow - never implements game logic

Every round calls all 3 tools in sequence: validate → resolve → update

### Tradeoffs Made
1. **Terminal-only UI** - Simple for ADK focus, gives up rich graphics
2. **Hardcoded 3 rounds** - Enforces requirement, less flexible
3. **Pattern-based AI** - Simple learning vs. neural networks
4. **No persistence** - Game doesn't save state between sessions

### Future Improvements (with more time)
- Multi-player support (2+ human players)
- Game statistics persistence (JSON file storage)
- Advanced AI with minimax algorithm
- Web UI option (Flask/Django) while keeping ADK core
- Unit tests for all tools
- Replay system (record/playback rounds)
- Different game variants (longer matches, team play)

---

**Status**: Production-ready. All requirements satisfied. Run `python3 main.py` to play.


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

## Status : Production-ready.
Run python main.py to play

