"""
config.py
---------
Central configuration for the PIN Security Research Platform.

This project is a self-contained simulation and training tool. It never
connects to, targets, or interacts with any real device, account, or
external authentication system. All "vaults" are local, in-memory or
SQLite-backed values you configure yourself.
"""

APP_NAME = "PIN Security Research Platform"
VERSION = "0.1.0-day1"

# Default lockout policy (wired up starting Day 2's lockout simulator)
DEFAULT_LOCKOUT_THRESHOLD = 5       # attempts allowed before lock
DEFAULT_BACKOFF_BASE_SECONDS = 2    # exponential backoff base

# Entropy / strength scoring weights (see backend/entropy.py)
# Pattern predictability is weighted more heavily than raw digit entropy:
# "1234" has maximal digit entropy (4 unique digits) but is one of the
# most guessed PINs in existence, so predictability must dominate the score.
MAX_SHANNON_ENTROPY_BITS = 2.0
ENTROPY_SCORE_WEIGHT = 30
PATTERN_SCORE_WEIGHT = 70
