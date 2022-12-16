import sys

def progress_bar(index, total, label):
    n_bar = 50  # Progress bar width
    progress = index / total
    sys.stdout.write('\r')
    sys.stdout.write(f"Loading: |{'█' * int(n_bar * progress):{n_bar}s}| {int(100 * progress)}%  {label}")
    sys.stdout.flush()
    
