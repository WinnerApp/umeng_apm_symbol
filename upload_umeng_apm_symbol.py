from urllib import response
import oss2
import charset_normalizer
import sys
import os
from dart_ops_engine import action_run, Env, DartOpsEngine
from dart_ops_engine.action_run import ActionRun, EnvGet, DictGet
from alibabacloud_umeng_apm20220214.client import Client as umeng_apm20220214Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_umeng_apm20220214 import models as umeng_apm_20220214_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient

# class UMengAPMSymbol(ActionRun):
#     def __init__(self):
#         pass

#     def run(self, env: Env, request: dict) -> dict:
#         config = models.Config(
#             # 必填，请确保代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_ID。,
#             access_key_id=EnvGet.read(env, 'ALIBABA_CLOUD_ACCESS_KEY_ID'),
#             # 必填，请确保代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_SECRET。,
#             access_key_secret=EnvGet.read(env, 'ALIBABA_CLOUD_ACCESS_KEY_SECRET'),
#         )
#         config.endpoint = f'apm.openapi.umeng.com'
#         self.client = Client(config)
#         self.client._open_platform_endpoint = f'apm.openapi.umeng.com'
#         pass

# class GetSymUploadParam(UMengAPMSymbol):
#     def __init__(self):
#         pass

#     def run(self, env: Env, request: dict) -> dict:
#         UMengAPMSymbol.run(self,env, request)
#         api = GetSymUploadParamRequest(
#             app_version=DictGet.read(request, 'app_version'),
#             data_source_id=DictGet.read(request, 'data_source_id'),
#             file_name=DictGet.read(request, 'file_name'),
#             file_type=DictGet.read(request, 'file_type'),
#         )
#         response = self.client.get_sym_upload_param_with_options(api,{}, util_models.RuntimeOptions())
#         return response.body.data.to_map()

class UploadSymbolFile(ActionRun):
    def __init__(self):
        pass

    

    def run(self, env: Env, request: dict) -> dict:
        client = self.create_client(
            EnvGet.read(env, 'ALIBABA_CLOUD_ACCESS_KEY_ID'),
            EnvGet.read(env, 'ALIBABA_CLOUD_ACCESS_KEY_SECRET'),
            )
        # 一定要设置 _open_platform_endpoint 参数
        client._open_platform_endpoint = f'apm.openapi.umeng.com'

        with open(DictGet.read(request, 'oss_url'), 'rb') as file:
            # 参数说明请参考接口文档
            upload_symbol_file_request = umeng_apm_20220214_models.UploadSymbolFileAdvanceRequest(
                app_version=DictGet.read(request, 'app_version'),
                data_source_id=DictGet.read(request, 'data_source_id'),
                file_name=DictGet.read(request, 'file_name'),
                file_type=DictGet.read(request, 'file_type'),
                oss_url_object=file
            )
            headers = {}
            try:
                # 复制代码运行请自行打印 API 的返回值
                client.upload_symbol_file_advance(upload_symbol_file_request, headers, util_models.RuntimeOptions())
                return {
                    "success": True
                }
            except Exception as error:
                # 如有需要，请打印 error
                UtilClient.assert_as_string(error.message)
        
    def create_client(
        self,
        access_key_id: str,
        access_key_secret: str,
    ) -> umeng_apm20220214Client:
        """
        使用AK&SK初始化账号Client
        @param access_key_id:
        @param access_key_secret:
        @return: Client
        @throws Exception
        """
        config = open_api_models.Config(
            # 必填，您的 AccessKey ID,
            access_key_id=access_key_id,
            # 必填，您的 AccessKey Secret,
            access_key_secret=access_key_secret
        )
        # Endpoint 请参考 https://api.aliyun.com/product/umeng-apm
        config.endpoint = f'apm.openapi.umeng.com'
        return umeng_apm20220214Client(config)

if __name__ == '__main__':
    engine = DartOpsEngine(description='upload umeng apm symbol')
    # engine.addAction('get_sym_upload_param', GetSymUploadParam(), description='获取符号上传参数')
    engine.addAction('upload_symbol_file', UploadSymbolFile(), description='上传符号文件')
    engine.run()
