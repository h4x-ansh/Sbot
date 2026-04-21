from collections import Counter
import sqlite3
from pathlib import Path

DB_PATH = Path("coin_flips.db")

def get_results_sequence(limit=50):
    """Get last N results as W/L sequence, ignoring chosen."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT result FROM coin_flips ORDER BY id DESC LIMIT ?;", (limit,))
    results = cursor.fetchall()
    conn.close()
    wl_seq = ['W' if r[0].lower() in ('won', 'w') else 'L' for r in results]
    return list(reversed(wl_seq))

def markov_predict(results_seq, orders=[2,3,4]):
    """Multi-order Markov chain prediction for next W/L.
    Returns (pred 'WIN'/'LOSS', confidence %, pattern str)"""
    if len(results_seq) < min(orders):
        return 'LOSS', 50, ''
    
    w_votes = 0.0
    total_weight = 0
    
    for order in orders:
        if len(results_seq) >= order:
            pattern = tuple(results_seq[-order:])
            follows = Counter()
            
            for i in range(len(results_seq) - order):
                if tuple(results_seq[i:i+order]) == pattern:
                    if i + order < len(results_seq):
                        follows[results_seq[i+order]] += 1
            
            if follows:
                prob_w = follows['W'] / sum(follows.values())
                weight = 5 - order
                w_votes += prob_w * weight
                total_weight += weight
    
    if total_weight == 0:
        return 'LOSS', 50, ' '.join(results_seq[-4:])
    
    avg_prob_w = w_votes / total_weight
    pred = 'WIN' if avg_prob_w > 0.5 else 'LOSS'
    conf = min(abs(avg_prob_w - 0.5) * 200, 100)
    
    # LOW DATA FIX: Penalize confidence if insufficient evidence
    if total_weight < 5:
        conf *= 0.5
    
    pattern = ' '.join(results_seq[-4:])
    
    return pred, conf, pattern

def get_last_choice():
    """Get last user's choice for decision logic."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT chosen FROM coin_flips ORDER BY id DESC LIMIT 1")
    last = cursor.fetchone()
    conn.close()
    if last:
        ch = last[0].lower()
        return 'heads' if 'head' in ch else 'tails'
    return 'heads'

def decision_from_prediction(pred, last_choice=None):
    """Convert WIN/LOSS pred to suggested choice (repeat/switch)."""
    import random
    if last_choice is None:
        last_choice = random.choice(["heads", "tails"])
    if pred == 'WIN':
        return last_choice
    else:
        return 'tails' if 'head' in last_choice else 'heads'
