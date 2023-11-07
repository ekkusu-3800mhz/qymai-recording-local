import obsws_python as obsws
from typing import Dict
import os


# 加载 OBS-Websocket 服务器配置

OBS_WS_HOST     = os.environ.get('OBS_WS_HOST', 'localhost')
OBS_WS_PORT     = os.environ.get('OBS_WS_PORT', '4455')
OBS_WS_PASSWORD = os.environ.get('OBS_WS_PASSWORD', '')
OBS_WS_TIMEOUT  = os.environ.get('OBS_WS_TIMEOUT', '30')


class OBSClient():

   
    ''' OBS Websocket Client

        Description: OBS-Websocket 接口调用封装
    '''


    def __init__(self):
        
        ''' 构造函数

            Description: 
                与 OBS-Websocket 服务器建立连接。
                OBS-Websocket 服务器配置从 .env 文件中获取。
        '''

        self.__client = obsws.ReqClient(host = OBS_WS_HOST, port = int(OBS_WS_PORT),
            password = OBS_WS_PASSWORD, timeout = int(OBS_WS_TIMEOUT))


    def get_version(self) -> Dict:

        ''' 获取版本信息

            Description:
                获取当前操作系统的环境和 OBS 程序的版本信息。

            Return:
                - <Dict> 含操作系统环境和 OBS 程序版本信息的字典
        '''

        res = self.__client.get_version()
        return {
            'OBSVersion': res.obs_version,
            'OBSWebSocketVersion': res.obs_web_socket_version,
            'RPCVersion': res.rpc_version,
            'Platform': res.platform,
            'PlatformDescription': res.platform_description,
        }


    def set_scene(self, scene_name: str):

        ''' 切换 OBS 场景（模板）

            Description:
                切换 OBS 场景模板，如单人机位画面或双人机位画面。

            Parameters:
                - scene_name: str 场景模板名称
        '''

        self.__client.set_current_program_scene(scene_name)


    def get_record_dir(self) -> str:

        ''' 获取录制文件保存路径

            Description:
                获取录制文件保存路径（一般为临时路径）。

            Return:
                - <str> 录制文件存储路径
        '''

        res = self.__client.get_record_directory()
        return res.record_directory
    

    def start_record(self):

        ''' 开始录制

            Description:
                操作 OBS 开始录制。
        '''

        self.__client.start_record()


    def stop_record(self) -> str:

        ''' 停止录制

            Description:
                操作 OBS 停止录制。

            Return:
                - <str> 录制保存文件名（含绝对路径）
        '''

        res = self.__client.stop_record()
        return res.output_path
