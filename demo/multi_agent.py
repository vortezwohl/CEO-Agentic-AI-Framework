from sympy import simplify
from dotenv import load_dotenv
from ceo import (
    Agent,
    Personality,
    get_openai_model,
    agentic,
    ability
)
from ceo.brain.hook import BeforeActionTaken, AfterActionTaken
from ceo.message import BeforeActionTakenMessage, AfterActionTakenMessage

load_dotenv()
model = get_openai_model()


@ability(model)
def calculator(expr: str) -> float:
    # this function only accepts a single math expression
    return simplify(expr)


@ability(model)
def write_file(filename: str, content: str) -> str:
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    return f'{content} written to {filename}.'


jack = Agent(abilities=[calculator], brain=model, name='Jack', personality=Personality.INQUISITIVE)
tylor = Agent(abilities=[write_file], brain=model, name='Tylor', personality=Personality.PRUDENT)


@agentic(jack)
def agent1():
    return


@agentic(tylor)
def agent2():
    return


def before_action_taken(agent: Agent, message: BeforeActionTakenMessage):
    print(f'Agent: {agent.name}, Next move: {message}')
    return message


def after_action_taken(agent: Agent, message: AfterActionTakenMessage):
    print(f'Agent: {agent.name}, Action taken: {message}')
    return message


if __name__ == '__main__':
    ceo = Agent(abilities=[agent1, agent2], brain=model, name='CEO', personality=Personality.INQUISITIVE)
    radius = '(10.01 * 10.36 * 3.33 / 2 * 16)'  # 2762.663904
    pi = 3.14159
    output_file = 'result.txt'
    request = f"Here is a sphere with radius of {radius} cm and pi here is {pi}, find the area and volume respectively then write the results into a file called '{output_file}'."
    result = ceo.assign(request).just_do_it(BeforeActionTaken(before_action_taken), AfterActionTaken(after_action_taken))  # area = 95910378.2949379, volume = 88322713378.13666
    print(f'Result: {result}')
