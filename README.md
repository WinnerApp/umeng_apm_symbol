## 上传Umeng符号表的命令行程序

## 打包

```bash
pyinstaller upload_umeng_apm_symbol.py
```

## 运行

```bash
export ALIBABA_CLOUD_ACCESS_KEY_ID=xxx
export ALIBABA_CLOUD_ACCESS_KEY_SECRET=xxx


upload_umeng_apm_symbol.py upload_symbol_file -
-args=app_version=1.0.0 --args=data_source_id=xxxxxxxxxxx --args=file_name=App.framework.dSYM.zip --args=file_type=3 --args=fl
utter_name=xxx --args=oss_url=xxx/xxxx/xxxx/xxx/xxxxxxx.zip
```
