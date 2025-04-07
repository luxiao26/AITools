from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_deepseek import ChatDeepSeek
from models.xiaohongshu_model import xiaohongshu
from Prompts.xiaohongshu_promt_template import system_template_text,user_template_text
import os
def generate_script(theme,api_key):
    # 提示词
    prompts = ChatPromptTemplate.from_messages([("system",system_template_text),
                                               ("user",user_template_text)])
    # 导入大模型
    model = ChatDeepSeek(model = "deepseek-chat",api_key = api_key)
    # 定义一个解析器   获得json格式输出，把输出解析为自定义类的实例
    output_parser = PydanticOutputParser(pydantic_object = xiaohongshu)
    chain = prompts | model | output_parser
    result = chain.invoke(
        {
            # 给ai的输出格式的指令
            "parser_instructions":output_parser.get_format_instructions(),
            # 来自用户的主题
            "theme":theme
        }
    )
    return result


# print(generate_script("大模型", os.getenv("DEEPSEEK_API_KEY")))