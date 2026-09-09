import sys


def state(capital: str):
    """Gets and prints capital city's state from known dicts."""
    states = {
        "Oregon": "OR",
        "Alabama": "AL",
        "New Jersey": "NJ",
        "Colorado": "CO"
    }
    capital_cities = {
        "OR": "Salem",
        "AL": "Montgomery",
        "NJ": "Trenton",
        "CO": "Denver"
    }

    if not isinstance(capital, str) or not capital:
        print("Unknown capital city")
        return

    inv_states = {val: key for key, val in states.items()}
    inv_capital_cities = {val: key for key, val in capital_cities.items()}

    short_state = inv_capital_cities.get(capital, None)
    if short_state is None:
        print("Unknown capital city")
        return

    state = inv_states.get(short_state, None)
    if state is None:
        print("Unknown capital city")
        return
    print(state)


if __name__ == '__main__':
    args = sys.argv
    if len(args) != 2:
        sys.exit()

    state(args[1])
