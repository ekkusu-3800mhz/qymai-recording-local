from django.views import View
from utils.obs_client import OBSClient
from utils.record_control import get_first_removable_device, move_video
from typing import Dict
from recording_local.settings import VIDEO_BUFFERING_TIME
import json
import time


def response(success: bool, data: Dict) -> Dict:
    res = {
        'success': success,
    }
    if data:
        res['data'] = data
    return json.dumps(res)


class BaseView(View):

    def get(self) -> str:
        return "Endpoint permission denied."
    
    def post(self):
        pass


class CheckEnvView(BaseView):

    def post(self) -> str:
        client: OBSClient = OBSClient()
        env: Dict = client.get_version()
        return response(True, {
            'env': env,
        })


class CheckDiskView(BaseView):

    def post(self) -> str:
        disk: str = get_first_removable_device()
        if disk:
            return response(True, {
                'device': disk,
            })
        else:
            return response(False, {
                'msg': 'Portable USB disk is not detected!',
            })
        

class SelectSceneView(BaseView):

    def post(self, scene_name: str) -> str:
        if not scene_name:
            return response(False, {
                'msg': 'Scene name is empty or invalid!',
            })
        client: OBSClient = OBSClient()
        client.set_scene(scene_name)
        return response(True)
    

class StartRecordView(BaseView):

    def post(self) -> str:
        disk: str = get_first_removable_device()
        if not disk:
            return response(False, {
                'msg': 'Portable USB disk is not detected!',
            })
        client: OBSClient = OBSClient()
        client.start_record()
        return response(True)
    

class StopRecordView(BaseView):

    def post(self) -> str:
        client: OBSClient = OBSClient()
        temp_video: str = client.stop_record()
        time.sleep(VIDEO_BUFFERING_TIME)
        disk: str = get_first_removable_device()
        if not disk:
            return response(False, {
                'msg': 'Portable USB disk is not detected!',
        })
        if move_video(temp_video, disk):
            return response(True)
        else:
            return response(False, {
                'msg': 'Failed to move video to your removable USB disk.',
            })
        