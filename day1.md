# 学习MetaGPT
## 1. 项目介绍

MetaGPT是一个基于LLM的优秀的多代理框架,将不同的角色分配给GPT模型，可以形成一个协作性软件公司。



## 2. 环境准备

个人使用poetry来安装环境，如果你没有安装poetry，可以参考[这里](https://python-poetry.org/docs/#installation)进行安装。

### 2.1 安装metagpt

教程说使用v0.4.0版本,我们在Pypi可以看到所有版本[点击查看](https://pypi.org/project/metagpt/#history)



```shell
poetry env use python3.10

poetry add metagpt==0.4.0

poetry  add python-dotenv
```
安装的时候提示错误：
```shell

The current project's Python requirement (>=3.10,<4.0) is not compatible with some of the required packages Python requirement:
  - qdrant-client requires Python >=3.7,<3.12, so it will not be satisfied for Python >=3.12,<4.0

Because metagpt (0.4.0) depends on qdrant-client (1.4.0) which requires Python >=3.7,<3.12, metagpt is forbidden.
So, because metagpt-learn depends on metagpt (0.4.0), version solving failed.

  • Check your dependencies Python requirement: The Python requirement can be specified via the `python` or `markers` properties
    
    For qdrant-client, a possible solution would be to set the `python` property to ">=3.10,<3.12"

    https://python-poetry.org/docs/dependency-specification/#python-restricted-dependencies,
    https://python-poetry.org/docs/dependency-specification/#using-environment-markers
```
然后我们许愿在项目文件中做限制，修改pyproject.toml文件
```shell
[tool.poetry.dependencies]
#增加个下面这一行
qdrant-client = { version = "1.4.0", python = ">=3.7,<3.12" }
```
安装的时候有 Installing loguru (0.6.0): Failed，我们许愿重新安装一遍
```shell
Package operations: 2 installs, 0 updates, 0 removals

  • Installing loguru (0.6.0)
  • Installing metagpt (0.4.0)
```

### 2.2 配置key
使用.env环境变量

```shell
OPENAI_API_KEY=sk-VmwaHlESnFjeNl
OPENAI_API_MODEL=gpt-3.5-turbo
```

## 3. Task1
注意把环境变量加载放在导入metagpt前面

```shell

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_MODEL"] = os.getenv("OPENAI_API_MODEL")
os.environ["OPENAI_API_BASE"] = "https://api.openai-forward.com/v1"

```
完整代码如下：
```python
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
```

运行结果，在使用GPT-3.5-turbo的时候，出现token不够的情况；换GPT-4模型后正常输出

疑问：

GPT-3.5和GPT-4生成的设计和代码差异比较大，谁的质量更好？

## 4. Task2
### 4.1 实现一个单动作Agent

注意对Role和Action类的继承和使用

```python
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_MODEL"] = os.getenv("OPENAI_API_MODEL")
os.environ["OPENAI_API_BASE"] = "https://api.openai-forward.com/v1"

import re
import asyncio
from metagpt.actions import Action

from metagpt.roles import Role
from metagpt.schema import Message
from metagpt.logs import logger

class SimpleWriteCode(Action):

    PROMPT_TEMPLATE = """
    Write a python function that can {instruction} and provide two runnnable test cases.
    Return ```python your_code_here ``` with NO other texts,
    your code:
    """

    def __init__(self, name="SimpleWriteCode", context=None, llm=None):
        super().__init__(name, context, llm)

    async def run(self, instruction: str):

        prompt = self.PROMPT_TEMPLATE.format(instruction=instruction)

        rsp = await self._aask(prompt)

        code_text = SimpleWriteCode.parse_code(rsp)

        return code_text

    @staticmethod
    def parse_code(rsp):
        pattern = r'```python(.*)```'
        match = re.search(pattern, rsp, re.DOTALL)
        code_text = match.group(1) if match else rsp
        return code_text

class SimpleCoder(Role):
    def __init__(
        self,
        name: str = "Alice",
        profile: str = "SimpleCoder",
        **kwargs,
    ):
        super().__init__(name, profile, **kwargs)
        self._init_actions([SimpleWriteCode])

    async def _act(self) -> Message:
        logger.info(f"{self._setting}: ready to {self._rc.todo}")
        todo = self._rc.todo # todo will be SimpleWriteCode()

        msg = self.get_memories(k=1)[0] # find the most recent messages

        code_text = await todo.run(msg.content)
        msg = Message(content=code_text, role=self.profile, cause_by=type(todo))

        return msg

async def main():
    msg = "写一个函数，接受1个整数参数，求1到那个整数之间到质数"
    role = SimpleCoder()
    logger.info(msg)
    result = await role.run(msg)
    logger.info(result)

if __name__ == "__main__":
    asyncio.run(main())
```

问题：这里的memoery如何持久化？


### 4.2 实现一个多动作Agent  

智能体的力量，或者说Role抽象的惊人之处，在于动作的组合（以及其他组件，比如记忆，但我们将把它们留到后面的部分）。
通过连接动作，我们可以构建一个工作流程，使智能体能够完成更复杂的任务.

让整体像一个流水线一样工作，每个角色都有自己的任务，然后把任务传递给下一个角色，最后完成任务。

```python


import asyncio
import os
import subprocess
import sys

from dotenv import load_dotenv

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_MODEL"] = os.getenv("OPENAI_API_MODEL")
os.environ["OPENAI_API_BASE"] = "https://api.openai-forward.com/v1"

import re
import asyncio

import sys
from metagpt.llm import LLM
from metagpt.actions import Action
from metagpt.roles import Role
from metagpt.schema import Message
from metagpt.logs import logger

class SimpleWriteCode(Action):

    PROMPT_TEMPLATE = """
    Write a python function that can {instruction} and provide two runnnable test cases.
    Return ```python your_code_here ``` with NO other texts,
    your code:
    """

    def __init__(self, name="SimpleWriteCode", context=None, llm=None):
        super().__init__(name, context, llm)

    async def run(self, instruction: str):

        prompt = self.PROMPT_TEMPLATE.format(instruction=instruction)

        rsp = await self._aask(prompt)

        code_text = SimpleWriteCode.parse_code(rsp)

        return code_text

    @staticmethod
    def parse_code(rsp):
        pattern = r'```python(.*)```'
        match = re.search(pattern, rsp, re.DOTALL)
        code_text = match.group(1) if match else rsp
        return code_text


class SimpleRunCode(Action):
    def __init__(self, name: str = "SimpleRunCode", context=None, llm: LLM = None):
        super().__init__(name, context, llm)

    async def run(self, code_text: str):
        result = subprocess.run([sys.executable, "-c", code_text], capture_output=True, text=True)
        code_result = result.stdout
        logger.info(f"{code_result=}")
        return code_result

class RunnableCoder(Role):
    def __init__(
        self,
        name: str = "Alice",
        profile: str = "RunnableCoder",
        **kwargs,
    ):
        super().__init__(name, profile, **kwargs)
        self._init_actions([SimpleWriteCode, SimpleRunCode])
        self._set_react_mode(react_mode="by_order")

    async def _act(self) -> Message:
        logger.info(f"{self._setting}: ready to {self._rc.todo}")
        # By choosing the Action by order under the hood
        # todo will be first SimpleWriteCode() then SimpleRunCode()
        todo = self._rc.todo

        msg = self.get_memories(k=1)[0] # find the most k recent messagesA
        result = await todo.run(msg.content)

        msg = Message(content=result, role=self.profile, cause_by=type(todo))
        self._rc.memory.add(msg)
        return msg

async def main():
    msg = "写一个函数，接受1个整数参数，求1到那个整数之间到质数"
    role = RunnableCoder()
    logger.info(msg)
    result = await role.run(msg)
    logger.info(result)

if __name__ == "__main__":
    asyncio.run(main())
```

### 4.4 实现一个更复杂的Agent：技术文档助手
在前文中我们已经介绍了如何实现一个简单的agent帮我们生成代码并执行代码，下面我们将带领大家实现更复杂的agent，并向大家展示MetaGPT中关于agent的更多设计细节
现在试着想想怎么让大模型为我们写一篇技术文档？
可能想到的是，我们告诉大模型：“请帮我生成关于Mysql的技术文档”，他可能很快地就能帮你完成这项任务，
但是受限于大模型自身的token限制，我们无法实现让他一次性就输出我们希望的一个完整的技术文档。
当然我们可以将我们的技术文档拆解成一个一个很小的需求，然后一个一个的提问，但是这样来说不仅费时，
而且还需要人工一直去跟他交互，非常的麻烦，下面我们就将利用MetaGPT框架来解决这个问题
我们利用上文中提到的agent框架来拆解我们的需求  

