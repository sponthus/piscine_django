import sys


def capital_city(state: str, states: dict, capital_cities: dict) -> str | None:
    """Gets and prints state's capital city from known dicts."""
    if not isinstance(state, str) or not state:
        return None

    short_state = states.get(state, None)
    if short_state is None:
        return None

    capital = capital_cities.get(short_state, None)
    if capital is None:
        return None
    return capital


def state(capital: str, states: dict, capital_cities: dict) -> str | None:
    """Gets and prints capital city's state from known dicts."""
    if not isinstance(capital, str) or not capital:
        return None

    inv_states = {val: key for key, val in states.items()}
    inv_capital_cities = {val: key for key, val in capital_cities.items()}

    short_state = inv_capital_cities.get(capital, None)
    if short_state is None:
        return None

    state = inv_states.get(short_state, None)
    if state is None:
        return None
    return state


def parse_args(args: str) -> list[str]:
    """
    Parses given args.

    - Gets first arg
    - Splits with coma
    - Returns the list of elements in arg
    """
    list_arg = args.split(",")
    res = []
    for element in list_arg:
        striped_element = element.strip()
        if striped_element:
            res.append(striped_element)
    return res


def all_in(args: str):
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

    lower_states = {}
    lower_capital_cities = {}
    for key, value in states.items():
        lower_states[key.lower()] = value
    for key, value in capital_cities.items():
        lower_capital_cities[key] = value.lower()

    values = parse_args(args)

    for value in values:
        res_state = state(
            value.lower(),
            states=lower_states,
            capital_cities=lower_capital_cities
        )
        res_capital = capital_city(
            value.lower(),
            states=lower_states,
            capital_cities=lower_capital_cities
        )

        if res_state is None and res_capital is None:
            print(value, "is neither a capital city nor a state")
        elif res_state is not None:
            print(
                value.capitalize(),
                "is the capital of",
                res_state.capitalize()
            )
        elif res_capital is not None:
            print(
                res_capital.capitalize(),
                "is the capital of",
                value.capitalize()
            )


if __name__ == '__main__':
    args = sys.argv
    if len(args) != 2:
        sys.exit()

    all_in(args[1])
