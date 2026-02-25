from collections import defaultdict

# position: points
_f1_points = defaultdict(
    lambda: 0,
    {
        1: 25,
        2: 18,
        3: 15,
        4: 12,
        5: 10,
        6: 8,
        7: 6,
        8: 4,
        9: 2,
        10: 1
    }
)

CHAMPIONSHIP_POINTS = {
    1: _f1_points
}