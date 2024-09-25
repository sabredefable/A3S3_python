import os
import json
import pandas as pd
from classes.AuditBuffer import AuditBuffer
from A3S3_ManifestExtractor import search_manifest

class A3S3_Auditor:
    def __init__(self, audit_file, output_dir, file_name):
        self._audit_file = audit_file
        self._audit_data = self.get_audit_data()
        self._output_dir = output_dir
        self._audit_name = self._audit_data['name']
        self._file_name = file_name

    def get_audit_data(self):
        if os.path.exists(self._audit_file):
            with open(self._audit_file, 'r') as f:
                json_temp = json.load(f)
        else:
            print("Audit file not found")
            return None
        return json_temp


    def start_auditing(self, audit_buffer):
        self._audit_data['file_name'] = self._file_name
        for control in self._audit_data['controls']:
            for audit_control in control['audit_controls']:
                if audit_control['source'].split('.')[0] == "Manifest":
                    audit_buffer.add(audit_control['source'], search_manifest(self._output_dir, audit_control['source'].split('.')[1]))

                source_temp = audit_buffer.get_features(audit_control['source'])
                for signal in audit_control['signals']:
                    if source_temp is not None:
                        if source_temp.has(signal['signal']):
                            signal['result'] = 1
                        else:
                            signal['result'] = 0
                    else:
                        signal['result'] = 'NA'

    def get_audited_data(self):
        return self._audit_data


    def export_audit_data(self, csv_export, xls_export, audit_buffer):
        json_output_file = self._output_dir + '/results.json'
        with open(json_output_file, 'w') as f:
            json.dump(self._audit_data, f, indent=4)
        fields = ["feature", "path_to_feature"]
        if csv_export == 1:
            print("Creating CSV file")
            for item in audit_buffer.get_items():
                csv_output_file = self._output_dir + '/'+item+'.csv'
                with open(csv_output_file, 'w') as f:
                    for i, item in enumerate(audit_buffer.get_items()):
                        df = pd.DataFrame({fields[j]: col for j, col in enumerate(audit_buffer.get_features(item))})
                        df.to_csv(f, index=False)
        if xls_export == 1:
            print("Creating Excel File")
            self.excel_export(self._audit_data, audit_buffer)

    def excel_export(self, audit_data, audit_buffer, only_result=False, output_dir=None, filename=None):
        fields = ["feature", "path_to_feature"]
        if output_dir is None:
            output_dir = self._output_dir
        if filename is None:
            filename = self._audit_name
        xls_output_file = output_dir + '/' + filename + '.xlsx'
        with pd.ExcelWriter(xls_output_file) as writer:
            df = pd.json_normalize(
                audit_data,
                record_path=['controls', 'audit_controls', 'signals'],  # Path to the nested 'signals'
                meta=[
                    'name', 'base', 'file_name',  # Top-level fields
                    ['controls', 'name'],
                    ['controls', 'sub'],
                    ['controls', 'audit_controls', 'source']  # Nested fields
                ],
                meta_prefix='meta_',  # Add a prefix to avoid conflicts with nested fields
                errors='ignore'  # Skip missing fields if any
            )

            # Save the DataFrame to an Excel file
            df.to_excel(writer, sheet_name="results", index=False)
            if not only_result:
                for i, item in enumerate(audit_buffer.get_items()):
                    df = pd.DataFrame({fields[j]: col for j, col in enumerate(audit_buffer.get_features(item))})
                    df.to_excel(writer, sheet_name=item, index=False)

    def get_audit_name(self):
        return self._audit_name
