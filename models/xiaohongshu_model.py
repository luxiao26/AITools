# 理想的解析数据
from typing import List
from pydantic import BaseModel,Field
# 继承basemodel   用field函数对数据进行校验
class xiaohongshu(BaseModel):
    # 定义标题和正文的属性
    # 标题有5个供用户选择，所以使用list
    # field给一个描述，               描述                  最小元素数量  最大元素数量
    titles:List[str] = Field(description="小红书的5个标题",min_length=5,max_length=5)
    content:str = Field(description="小红书的正文内容")
