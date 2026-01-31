# Chess Game Developer Guide

This document provides an overview of the high-level architecture and component interactions in the Chess game implementation.

## Architecture Overview

The Chess game is built with a modular architecture that separates concerns for better maintainability, testability, and extensibility. The main components are:

- **Game Logic**: Handles the rules, state, and moves
- **Rendering**: Manages visual output
- **Input Handling**: Processes user input
- **Asset Management**: Loads and provides game assets
- **Rules Engine**: Validates moves and game states

## Core Components

### GameState (`game_state.py`)
Centralizes all game state including:
- Board state
- Player information
- Current turn
- Game result
- Asset and rules validators

### Board (`board.py`)
Represents the chess board with:
- 8x8 grid of squares
- Piece placement
- King tracking
- Promotion handling

### Player (`player.py`)
Manages player-specific logic:
- Legal move calculation
- Move execution
- Game status checking

### Pieces (`pieces.py`)
Defines piece behavior:
- Geometric movement patterns
- Piece-specific rules
- Image assets

### Rendering (`renderer.py`)
Handles all visual output:
- Board drawing
- Piece rendering
- Game end screens
- UI elements

### Input Handling (`input_handler.py`)
Processes pygame events into game commands:
- Mouse clicks
- Keyboard input
- Quit commands

### Asset Management (`assets.py`)
Manages game assets:
- Piece images
- Configurable paths
- Centralized loading

### Rules Engine (`rules_engine.py`)
Validates game rules:
- Check detection
- Attack validation
- Move legality

## Component Interactions

```
User Input -> InputHandler -> GameState -> Player/Board -> Rules Engine
                                      |
                                      v
                                 Renderer -> Display
                                      ^
                                      |
                                 AssetManager
```

1. **Input Processing**: `InputHandler` converts pygame events to command objects
2. **Game Logic**: `GameState` coordinates between players, board, and validators
3. **Move Validation**: `Rules Engine` ensures moves are legal
4. **State Updates**: `Board` and `Player` update internal state
5. **Rendering**: `Renderer` draws the current state using assets from `AssetManager`

## Key Design Principles

- **Separation of Concerns**: Each component has a single responsibility
- **Dependency Injection**: Components receive dependencies rather than creating them
- **Type Safety**: Comprehensive type annotations for reliability
- **Testability**: Modular design enables isolated testing
- **Configurability**: Assets and constants are centralized and configurable

## Development Workflow

1. Modify game logic in respective components
2. Update types and ensure mypy compliance
3. Run golden master tests to verify behavior
4. Update documentation as needed

## Testing

The project uses a Golden Master testing approach with `tests/test_golden_master.py` to ensure refactoring preserves game behavior.