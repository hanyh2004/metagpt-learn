import asyncio
import os
from dotenv import load_dotenv

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_MODEL"] = os.getenv("OPENAI_API_MODEL")
os.environ["OPENAI_API_BASE"] = "https://api.openai-forward.com/v1"

from metagpt.roles import (
    Architect,
    Engineer,
    ProductManager,
    ProjectManager,
)
from metagpt.team import Team


async def startup(idea: str):
    company = Team()
    company.hire(
        [
            ProductManager(),
            Architect(),
            ProjectManager(),
            Engineer(),
        ]
    )
    company.invest(investment=3.0)
    company.start_project(idea=idea)

    await company.run(n_round=5)

if __name__ == '__main__':
    asyncio.run(startup(idea="write a cli blackjack game")) # blackjack: 二十一点
