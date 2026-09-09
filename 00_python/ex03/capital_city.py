import sys


def capital_city(state: str):
    """Gets and prints state's capital city from known dicts."""
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

    if not isinstance(state, str) or not state:
        print("Unknown state")
        return

    short_state = states.get(state, None)
    if short_state is None:
        print("Unknown state")
        return

    capital = capital_cities.get(short_state, None)
    if capital is None:
        print("Unknown state")
        return
    print(capital)


if __name__ == '__main__':
    args = sys.argv
    if len(args) != 2:
        sys.exit()

    capital_city(args[1])
