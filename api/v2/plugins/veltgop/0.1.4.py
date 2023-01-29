from khl import Bot, Message
import asyncio
import os
import logging
import datetime
import requests
import json
import wget
from khl.card import CardMessage, Card
from logging import handlers

#日志
logger = logging.getLogger('test')
logger.setLevel(level=logging.INFO)
#设置日志格式
formatter = logging.Formatter('[%(levelname)s][%(asctime)s]: %(message)s')
#注册控制台输出
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(formatter)
#注册文件输出
time_rotating_file_handler = handlers.TimedRotatingFileHandler(filename='./logs/kook-spelako.log', when='S', encoding='utf-8')
time_rotating_file_handler.setLevel(logging.INFO)
time_rotating_file_handler.setFormatter(formatter)
#完成注册
logger.addHandler(time_rotating_file_handler)
logger.addHandler(stream_handler)


#载入配置
with open('./config/config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

#检查更新
Network_Ver = requests.get("https://diamond-weiqu.github.io/api/v2/plugins/veltgop/KookBot-spelako.txt")
CheckVer = json.loads(Network_Ver.text)
NowVer = '0.1.4'
if NowVer==CheckVer['Ver']:
    logger.info('已检查更新！当前版本:'+NowVer+' 最新版本:'+CheckVer['Ver']+'已是最新！')
else:
    logger.warning('已检查更新！当前版本:'+NowVer+' 最新版本:'+CheckVer['Ver']+'不是最新！正在自动下载最新版本！')
    wget.download("https://diamond-weiqu.github.io/api/v2/plugins/veltgop/"+CheckVer['Ver']+".py", "./")
    logger.warning("更新完毕！请重启Bot！")
    exit(0)
#检查登陆TOKEN
if config['token']=="":
    logger.critical('TOKEN为空！已取消登录！')
    exit(0)
else:
    bot = Bot(token=config['token'])
    logger.info('已读取配置TOKEN!正在登陆...')
adminlist = config['admin']

for admins in list(adminlist):
    logger.info('已加载管理员: '+admins+' ')
#初始化查询
os.chdir('./lib/SpelakoCLI-1.0.0/')

# register command
@bot.command(regex=r'[\s\S]*')
async def foo(msg: Message):
    logger.info('收到一条消息！-->'+msg.author_id+':'+msg.content+'['+msg.target_id+']')
    if msg.content == '测试通信':
         await msg.reply('通信正常！')
         logger.info('收到一条测试通信！发送者:'+msg.author_id)
         logger.info('发送一条消息！<--通信正常')
    if msg.content == '!!admin clean':
        for admins in list(adminlist):
            if msg.author_id==admins:
                
                cmd = 'php SpelakoCLI.php --core="../SpelakoCore-22w30a/SpelakoCore.php" --config="config.json" --yolo="/spelako clean"'
                res = os.popen(cmd)
                zhuanma_str = res.buffer.read().decode(encoding='utf8')
                #print(zhuanma_str)
                await msg.reply(f'管理员'+admins+'您好！执行结果如下：\n'+zhuanma_str)
                logger.info('发送一条消息！<--'+'管理员'+admins+'您好！执行结果如下：\n'+zhuanma_str)
            
    if msg.content == '!!admin help':
        for admins in list(adminlist):
            if msg.author_id==admins:
                
                cmd = 'php SpelakoCLI.php --core="../SpelakoCore-22w30a/SpelakoCore.php" --config="config.json" --yolo="/spelako help"'
                res = os.popen(cmd)
                zhuanma_str = res.buffer.read().decode(encoding='utf8')
                #print(zhuanma_str)
                await msg.reply(f'管理员'+admins+'您好！执行结果如下：\n'+zhuanma_str)
                logger.info('发送一条消息！<--'+'管理员'+admins+'您好！执行结果如下：\n'+zhuanma_str)
            
    if msg.content == '!!admin stats':
        for admins in list(adminlist):
            if msg.author_id==admins:
                
                cmd = 'php SpelakoCLI.php --core="../SpelakoCore-22w30a/SpelakoCore.php" --config="config.json" --yolo="/spelako stats"'
                res = os.popen(cmd)
                zhuanma_str = res.buffer.read().decode(encoding='utf8')
                #print(zhuanma_str)
                await msg.reply(f'管理员'+admins+'您好！执行结果如下：\n'+zhuanma_str)
                logger.info('发送一条消息！<--'+'管理员'+admins+'您好！执行结果如下：\n'+zhuanma_str)
            


@bot.command()
async def hyp(msg: Message, player_id: str='', game: str='', mode: str=''):
        
        cmd = 'php SpelakoCLI.php --core="../SpelakoCore-22w30a/SpelakoCore.php" --config="config.json" --yolo="'+msg.content+'"'
        res = os.popen(cmd)
        zhuanma_str = res.buffer.read().decode(encoding='utf8')
        #print(zhuanma_str)
        await msg.reply(zhuanma_str)
        logger.info('发送一条消息！<--'+zhuanma_str)


# invoke this via saying `/hello` in channel
@bot.command(name='hello')
async def world(msg: Message):  # when `name` is not set, the function name will be used

    await msg.reply('world!')
    logger.info('发送一条消息！<--'+'world!')



# everything done, go ahead now!
logger.info('登录成功！')
bot.run()
