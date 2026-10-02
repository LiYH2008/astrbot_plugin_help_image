import os
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
import astrbot.api.message_components as Comp

@register("help_image", "YourName", "发送 /help 指令返回自定义帮助图片", "1.0.0")
class HelpImage(Star):
    def __init__(self, context: Context):
        super().__init__(context)
    
    @filter.command("help") 
    async def handle_help(self, event: AstrMessageEvent):
        '''发送 /help 指令返回自定义帮助图片'''
        
        # 1. 获取 main.py 所在的绝对路径
        # 无论插件被解压到哪里，这行代码都能找到当前文件夹
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # 2. 拼接图片路径
        # 假设图片在 main.py 同级的 images 文件夹里
        image_path = os.path.join(current_dir, "images", "custom_help.png")
        
        # 打印日志，方便你在控制台看它到底在找哪个路径
        logger.info(f"正在读取图片路径: {image_path}")

        if not os.path.exists(image_path):
            # 如果找不到，尝试找一下 jpg
            image_path = os.path.join(current_dir, "images", "custom_help.jpg")
            if not os.path.exists(image_path):
                logger.error(f"图片文件丢失: {image_path}")
                yield event.plain_result(f"错误：找不到图片文件。程序试图读取: {image_path}")
                return

        # 3. 构建消息链 (符合官方文档标准)
        chain = [
            Comp.Image.fromFileSystem(image_path)
        ]
        
        # 4. 返回结果
        yield event.chain_result(chain)