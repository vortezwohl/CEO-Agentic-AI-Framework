import sys

import sympy
from dotenv import load_dotenv

from ceo import Agent, get_openai_model, agentic, ability

load_dotenv()
sys.set_int_max_str_digits(10**8)

model = get_openai_model()


@ability
def calculator(expr: str) -> float | str:
    # this function only accepts a single math expression
    try:
        try:
            return f'{expr} equals to {sympy.simplify(expr, rational=None)}'
        except ValueError as ve:
            return ve.__repr__()
    except sympy.SympifyError as se:
        return se.__repr__()


@ability
def write_file(filename: str, content: str) -> str:
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    return f'{content} written to {filename}.'


@agentic(Agent(abilities=[calculator], brain=model, name='Jack', p=0.05, beta=1.2))
def agent1():
    return


@agentic(Agent(abilities=[write_file], brain=model, name='Tylor', p=0.05, beta=1.2))
def agent2():
    return


if __name__ == '__main__':
    ceo = Agent(abilities=[agent1, agent2], brain=model, name='test', p=0.05, beta=1.2)
    print(ceo.name)
    result = ceo.assign("Here is a sphere with a radius of (1 * 9.5 / 2 * 2) cm and pi here is 3.14159, "
                 "find the area and volume respectively, "
                 "then write the results into a file called 'result.txt'.").just_do_it()
    print(result)
