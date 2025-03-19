import subprocess
import os
import json

class A3S3_Decompilers:
    def __init__(self):
        self.option = ""
        self.command = ""
        self.output_dir = ""
        self.apk_path = ""
        self.apk_name = ""

    def get_options(self):
        options = ["jadx"]
        return options

    def set_option(self, option, output_dir, apk_path):
        self.output_dir = output_dir
        self.apk_path = apk_path
        self.option = option
        if option == "jadx":
            self.command = ["jadx", "-d", self.output_dir, self.apk_path]

    def decompile_apk(self, check_exist=False):
        if self.apk_path.endswith(".xapk"):
            self.output_dir = self.output_dir
            print(f"XAPK {self.apk_path}")
            unzip_command = ["unzip", self.apk_path, "-d", self.output_dir]
            if check_exist:
                if os.path.exists(self.output_dir):
                    print(".xapk is already unzipped")
                else:
                    subprocess.run(unzip_command, check=True)
            else:
                subprocess.run(unzip_command, check=True)
            pre_manifest = f"{self.output_dir}/manifest.json"
            if os.path.exists(pre_manifest):
                with open(pre_manifest, 'r') as f:
                    json_temp = json.load(f)
            for file in json_temp["split_apks"]:
                if file["id"] == "base":
                    apk_path = f"{self.output_dir}/{file['file']}"
            self.set_option(self.option, self.output_dir, apk_path)
        if check_exist:
            if os.path.isdir(f"{self.output_dir}/sources"):
                print("File already decompiled")
            else:
                subprocess.run(self.command, capture_output=True, text=True)
        else:
            subprocess.run(self.command, capture_output=True, text=True)
