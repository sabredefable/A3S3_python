import os
import re
from classes.ListWithPaths import ListWithPaths
from classes.AuditBuffer import AuditBuffer


class A3S3_FeaturesExtractor:
    def __init__(self):
        self.output_dir = ""
        self.imports = ListWithPaths()
        self.packages = ListWithPaths()
        self.urls = ListWithPaths()
        self.option = ""
        self.audit_buffer = AuditBuffer()

    def extract_features(self, output_dir, extractor, verbose):
        self.output_dir = output_dir + '/sources'
        self.option = extractor

        if os.path.exists(self.output_dir):
            for path, subdirs, files in os.walk(self.output_dir):
                for name in files:
                    if name.endswith('.java'):
                        with open(os.path.join(path, name)) as f:
                            for rawLine in f.readlines():
                                if rawLine.startswith("import"):
                                    line = rawLine.split(" ")[1].strip()[:-1]
                                    if line not in self.imports.names:
                                        self.imports.add(line, os.path.join(path, name)[len(self.output_dir):])
                                        if verbose:
                                            print("Added " + line + " to imports")
                                elif rawLine.startswith("package"):
                                    line = rawLine.split(" ")[1].strip()[:-1]
                                    if line not in self.packages.names:
                                        self.packages.add(line, os.path.join(path, name)[len(self.output_dir):])
                                        if verbose:
                                            print("Added " + line + " to packages")
                                elif self.find_urls(rawLine):
                                    for url in self.find_urls(rawLine):
                                        self.urls.add(url, os.path.join(path, name)[len(self.output_dir):])
                                        if verbose:
                                            print("Added " + url + " to URLs")

            self.audit_buffer.add("Android.packages", self.packages)
            self.audit_buffer.add("Android.imports", self.imports)
            self.audit_buffer.add("Android.urls", self.urls)
        else:
            print(self.output_dir + " does not exist")
        return self.audit_buffer


    def find_urls(self, line):
        pattern = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
        urls = re.findall(pattern, line)
        return [url[0] for url in urls]