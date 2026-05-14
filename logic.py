# Class to track score and game state

class GameTracker:
    def __init__(self):
        self.score = 0
        self.reset_game()

    def reset_game(self):
        self.found = set()
        self.misses = 0
        self.max_misses = 3
        self.is_over = False

    def check_hit(self, px, py, diffs):
        if self.is_over:
            return None, False

        for i, (dx, dy, dw, dh) in enumerate(diffs):
            if i in self.found:
                continue
            
            # See if the click is inside the box (with a little bit of extra room)
            gap = 20
            if (dx - gap <= px <= dx + dw + gap) and (dy - gap <= py <= dy + dh + gap):
                self.found.add(i)
                self.score += 1
                return i, True
        
        # Didn't find anything
        self.misses += 1
        if self.misses >= self.max_misses:
            self.is_over = True
        return None, False
