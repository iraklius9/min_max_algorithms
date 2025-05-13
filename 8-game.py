import random
import heapq
from typing import List, Tuple

GOAL_STATE = [1, 2, 3, 4, 5, 6, 7, 8, 0]


def print_board(state: List[int]):
    for i in range(0, 9, 3):
        print(state[i:i + 3])
    print()


def is_solvable(state: List[int]) -> bool:
    inv_count = 0
    for i in range(8):
        for j in range(i + 1, 9):
            if state[i] and state[j] and state[i] > state[j]:
                inv_count += 1
    return inv_count % 2 == 0


def generate_puzzle() -> List[int]:
    state = list(range(9))
    while True:
        random.shuffle(state)
        if is_solvable(state):
            return state


def manhattan_distance(state: List[int]) -> int:
    distance = 0
    for i in range(9):
        if state[i] == 0:
            continue
        x1, y1 = divmod(i, 3)
        x2, y2 = divmod(state[i] - 1, 3)
        distance += abs(x1 - x2) + abs(y1 - y2)
    return distance


def get_neighbors(state: List[int]) -> List[Tuple[List[int], str]]:
    neighbors = []
    index = state.index(0)
    x, y = divmod(index, 3)
    moves = {
        "Up": (-1, 0),
        "Down": (1, 0),
        "Left": (0, -1),
        "Right": (0, 1)
    }

    for move, (dx, dy) in moves.items():
        nx, ny = x + dx, y + dy
        if 0 <= nx < 3 and 0 <= ny < 3:
            new_index = nx * 3 + ny
            new_state = state[:]
            new_state[index], new_state[new_index] = new_state[new_index], new_state[index]
            neighbors.append((new_state, move))
    return neighbors


def a_star(start: List[int]) -> Tuple[List[List[int]], List[str]]:
    frontier = []
    heapq.heappush(frontier, (manhattan_distance(start), 0, start, []))
    explored = set()

    while frontier:
        _, cost, state, path = heapq.heappop(frontier)
        if state == GOAL_STATE:
            return path, [state]

        explored.add(tuple(state))

        for neighbor, move in get_neighbors(state):
            if tuple(neighbor) in explored:
                continue
            new_cost = cost + 1
            heapq.heappush(frontier,
                           (new_cost + manhattan_distance(neighbor), new_cost, neighbor, path + [(state, move)]))

    return [], []


def main():
    start_state = generate_puzzle()
    print("🔢 Initial State:")
    print_board(start_state)
    path, steps = a_star(start_state)

    if not path:
        print("No solution found.")
        return

    print("✅ Solution Found!")
    print("Number of moves:", len(path))
    print("Moves:")
    for idx, (state, move) in enumerate(path):
        print(f"{idx + 1}. Move {move}")
        current = state
        print_board(current)

    print("🏁 Goal State:")
    print_board(GOAL_STATE)


if __name__ == "__main__":
    main()


"""
აღწერა:

1. თავსატეხის გენერირება:
- გენერირდება 8 ფილის შემთხვევითი განლაგება და ცარიელი ადგილი.
- ყველა შესაძლო კონფიგურაციის მხოლოდ 50% არის ამოხსნადი.
- სკრიპტი იყენებს „ინვერსიების“ კონცეფციას ამოხსნადობის შესამოწმებლად.
- თუ ინვერსიების რაოდენობა ლუწია, თავსატეხი ამოხსნადია.

2. ძიების ალგორითმი:
- A* ძიების ალგორითმი გამოიყენება საწყისი მდგომარეობიდან მიზნის მდგომარეობამდე ოპტიმალური გზის მოსაძებნად.
- პრიორიტეტული რიგი (მინიმალური გროვა) გამოიყენება ძიების კვანძების საზღვრის სამართავად.

3. ევრისტიკა:
- მანჰეტენის მანძილი გამოიყენება როგორც ევრისტული ფუნქცია.
- ის აჯამებს ჰორიზონტალური და ვერტიკალური გადაადგილებების რაოდენობას, რომლითაც თითოეული ფილი დაშორებულია მისი მიზნის პოზიციიდან.
- ეს ევრისტიკა დასაშვები და თანმიმდევრულია, რაც A*-ს ამ ამოცანისთვის სრულს და ოპტიმალურს ხდის.

4. მოძრაობა:
- ცარიელი სივრცე (0) შეიძლება გადაადგილდეს ოთხი მიმართულებით: ზემოთ, ქვემოთ, მარცხნივ ან მარჯვნივ.
- სწორი მეზობლები გენერირდება ცარიელი ადგილის შეცვლით. მიმდებარე ფილასთან ერთად.

5. შედეგი:
- სკრიპტი აჩვენებს შემთხვევით გენერირებულ საწყის თავსატეხის მდგომარეობას.
- თუ ამოხსნადია, ის ბეჭდავს სვლების და ეტაპობრივი გადასვლების რაოდენობას მიზნის მდგომარეობის მისაღწევად.
- ნაჩვენებია საბოლოო მიზნის მდგომარეობა.
"""
