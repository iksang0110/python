import sys
input = sys.stdin.read

def solve():
    data = input().split()
    N = int(data[0])
    V = int(data[1]) - 1  # 0-based index
    M = int(data[2])
    
    # node values
    values = list(map(int, data[3:3+N]))
    
    # queries
    queries = list(map(int, data[3+N:]))
    
    cycle_start = V
    cycle_length = N - V
    
    # Answer each query
    results = []
    for q in queries:
        if q < N:
            results.append(values[q])
        else:
            # Calculating position in the cycle
            q = cycle_start + (q - cycle_start) % cycle_length
            results.append(values[q])
    
    # Print results
    for result in results:
        print(result)

solve()
