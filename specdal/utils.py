import pandas as pd

def get_monotonic_series(series):
    """return a list of series with monotonic index
    
    TODO: test what happens if not strictly monotonic
        i.e. index: 1, 2, 3, 3
    """
    if series.index.is_monotonic:
        return [series]
    else:
        index = pd.Series(series.index)
        head_positions = index[index.diff() < 0].index

        N = head_positions.size
        
        result = [series.iloc[:head_positions[0]]]
        result += [series.iloc[head_positions[i]:head_positions[i+1]] for i in range(0, N-1)]
        result += [series.iloc[head_positions[N-1]:]]
        return result
