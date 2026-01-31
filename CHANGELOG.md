# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/SemVer).

## [1.0.0] - 2023-10-01

### Added
- Initial release of the Chess game
- Basic chess rules implementation
- Pygame-based GUI
- Piece movements, check/checkmate detection, castling, pawn promotion
- Regression tests with Golden Master approach
- Comprehensive type annotations
- Asset management system
- Rules engine for move validation
- Modular architecture with separated concerns

### Changed
- Refactored code for better maintainability
- Centralized constants and assets
- Separated rendering from game logic
- Abstracted input handling
- Moved legality checks to dedicated rules engine

### Technical Improvements
- Added type hints throughout the codebase
- Implemented AssetManager for configurable piece images
- Created ChessRenderer for rendering logic
- Introduced InputHandler for event processing
- Centralized game state in GameState class
- Rules validation in MoveValidator class