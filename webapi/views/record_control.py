from django.views import View
from django.http import HttpRequest, JsonResponse
from obsws_python.error import OBSSDKRequestError
from utils.obs_client import OBSClient
from utils.record_control import get_first_removable_device, move_video
from typing import Dict
from recording_local.settings import VIDEO_BUFFERING_TIME
import time


def response(success: bool, data: Dict = {}) -> Dict:
    res = {
        'success': success,
    }
    if data:
        res['data'] = data
    return res


class BaseView(View):

    def get(self, request: HttpRequest) -> JsonResponse:
        return JsonResponse("Endpoint permission denied.")
    
    def post(self, request: HttpRequest):
        pass


class CheckEnvView(BaseView):

    def post(self, request: HttpRequest) -> JsonResponse:
        try:
            client: OBSClient = OBSClient()
            env: Dict = client.get_version()
            return JsonResponse(response(True, {
                'env': env,
            }))
        except OBSSDKRequestError as error:
            return JsonResponse(response(False, {
                'msg': str(error),
            }))


class CheckDiskView(BaseView):

    def post(self, request: HttpRequest) -> JsonResponse:
        try:
            disk: str = get_first_removable_device()
            if disk:
                return JsonResponse(response(True, {
                    'device': disk,
                }))
            else:
                return JsonResponse(response(False, {
                    'msg': 'Portable USB disk is not detected!',
                }))
        except OBSSDKRequestError as error:
            return JsonResponse(response(False, {
                'msg': str(error),
            }))
        

class SelectSceneView(BaseView):

    def post(self, request: HttpRequest) -> JsonResponse:
        try:
            scene_name: str = request.POST.get('scene_name', None)
            if not scene_name:
                return JsonResponse(response(False, {
                    'msg': 'Scene name is empty or invalid!',
                }))
            client: OBSClient = OBSClient()
            client.set_scene(scene_name)
            return JsonResponse(response(True))
        except OBSSDKRequestError as error:
            return JsonResponse(response(False, {
                'msg': str(error),
            }))
    

class StartRecordView(BaseView):

    def post(self, request: str) -> JsonResponse:
        try:
            disk: str = get_first_removable_device()
            if not disk:
                return JsonResponse(response(False, {
                    'msg': 'Portable USB disk is not detected!',
                }))
            client: OBSClient = OBSClient()
            client.start_record()
            return JsonResponse(response(True))
        except OBSSDKRequestError as error:
            msg: (str or None) = None
            if error.code == 500:
                msg = 'OBS was already started recording!'
            else:
                msg = str(error)
            return JsonResponse(response(False, {
                'msg': msg,
            }))
    

class StopRecordView(BaseView):

    def post(self, request: HttpRequest) -> JsonResponse:
        try:
            disk: (str or None) = get_first_removable_device()
            if not disk:
                return JsonResponse(response(False, {
                    'msg': 'Portable USB disk is not detected!',
            }))
            disk = None
            client: OBSClient = OBSClient()
            temp_video: str = client.stop_record()
            time.sleep(int(VIDEO_BUFFERING_TIME))
            disk = get_first_removable_device()
            if not disk:
                return JsonResponse(response(False, {
                    'msg': 'Portable USB disk is not detected!',
            }))
            if move_video(temp_video, disk):
                return JsonResponse(response(True))
            else:
                return JsonResponse(response(False, {
                    'msg': 'Failed to move video to your removable USB disk.',
                }))
        except OBSSDKRequestError as error:
            msg: (str or None) = None
            if error.code == 501:
                msg = 'OBS was already stopped recording!'
            else:
                msg = str(error)
            return JsonResponse(response(False, {
                'msg': msg,
            }))
        