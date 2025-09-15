from typing import List
import json

FPS_TO_EMF = {
    36: 164,
    18: 84,
    9: 48,
    1: 1
}

class Solution:
    def __init__(self, data_file_path: str, protocol_json_path: str):
        self.data_file_path = data_file_path
        self.protocol_json_path = protocol_json_path

    def get_supported_protocols(self, protocol_json_path: str, version: str) -> List[str]:
        """
        Get all supported protocols for a given version, always in HEX format
        """
        with open(protocol_json_path, 'r') as f:
            protocol_data = json.load(f)
        
        if version not in protocol_data["protocols_by_version"]:
            return []
        
        protocols = protocol_data["protocols_by_version"][version]["protocols"]
        id_type = protocol_data["protocols_by_version"][version]["id_type"]
        
        # Convert to HEX format if needed
        if id_type == "dec":
            return [f"0x{int(protocol):x}" for protocol in protocols]
        else:  # id_type == "hex"
            return protocols

       

    # Question 1: What is the version name used in the communication session?
    def q1(self) -> str:
        hex_message_data_version = self.get_message_data(self.data_file_path, '0x1')
        if hex_message_data_version is None:
            return "Version not found"
        # Remove spaces from hex string for conversion
        hex_clean = hex_message_data_version.replace(' ', '')
        version_str = self.hex_to_ascii(hex_clean)
        return version_str

    # Question 2: Which protocols have wrong messages frequency in the session compared to their expected frequency based on FPS?
    def q2(self) -> List[str]:
        list_wrong_frequency = []
        version = self.q1()
        if version == "Version not found":
            return []
            
        dict_protocols = self.count_protocols_in_data(self.data_file_path)
        
        with open(self.protocol_json_path, 'r') as f:
            protocol_data = json.load(f)
        
        if version not in protocol_data["protocols_by_version"]:
            return []
            
        version_protocols = self.get_supported_protocols(self.protocol_json_path, version)
        
        for protocol in dict_protocols:
            if protocol not in version_protocols:
                print(f"protocol {protocol} are not supported in version {version}")
            elif protocol in protocol_data["protocols"]:
                expected_fps = protocol_data["protocols"][protocol]["fps"]
                expected_emf = FPS_TO_EMF.get(expected_fps)
                actual_count = dict_protocols[protocol]
                if expected_emf != actual_count:
                    list_wrong_frequency.append(protocol)
        return list_wrong_frequency      
            
            

    # Question 3: Which protocols are listed as relevant for the version but are missing in the data file?
    def q3(self) -> List[str]:
        version = self.q1()
        if version == "Version not found":
            return []
        version_protocols = self.get_supported_protocols(self.protocol_json_path, version)
        dict_key_protocols = self.count_protocols_in_data(self.data_file_path).keys()
        return [protocol for protocol in version_protocols if protocol not in dict_key_protocols] 
        

    # Question 4: Which protocols appear in the data file but are not listed as relevant for the version?
    def q4(self) -> List[str]:
        version = self.q1()
        if version == "Version not found":
            return []
        version_protocols = self.get_supported_protocols(self.protocol_json_path, version)
        dict_key_protocols = self.count_protocols_in_data(self.data_file_path).keys()
        return [protocol for protocol in dict_key_protocols if protocol not in version_protocols]

    # Question 5: Which protocols have at least one message in the session with mismatch between the expected size integer and the actual message content size?
    def q5(self) -> List[str]:
        with open(self.data_file_path, 'r') as file:
            protocols_mismatch_size = set()
            for line in file:
                parts = line.split(", ")
                if len(parts) < 4:
                    continue
                try:
                    protocol_id = parts[2]
                    if protocol_id in protocols_mismatch_size:
                        continue           
                    size = int(parts[3].split()[0])
                    message = ' '.join(parts[-1].split())
                    hex_values = message.split()
                    size_in_bytes = len(hex_values)
                    if size_in_bytes != size:
                        protocols_mismatch_size.add(protocol_id)
                except (IndexError, ValueError) as e:
                    # Skip lines that can't be parsed properly
                    continue

            return list(protocols_mismatch_size)

    # Question 6: Which protocols are marked as non dynamic_size in protocol.json, but appear with inconsistent expected message sizes Integer in the data file?
    def q6(self) -> List[str]:
        with open(self.protocol_json_path, 'r') as f:
            protocol_data = json.load(f)
        non_dynamic_protocols_mismatch = []
        protocols_mismatch_size = self.q5()
        for protocol in protocols_mismatch_size:
            if protocol in protocol_data["protocols"] and protocol_data["protocols"][protocol]["dynamic_size"] == False:
                non_dynamic_protocols_mismatch.append(protocol)

        return non_dynamic_protocols_mismatch

    @staticmethod
    def hex_to_ascii(hex_string):
        """
        Convert a hexadecimal string to its ASCII representation.
        """
        if len(hex_string) % 2 != 0:
            hex_string = '0' + hex_string
            
        ascii_string = ''.join(chr(int(hex_string[i:i + 2], 16)) for i in range(0, len(hex_string), 2))
        return ascii_string



    @staticmethod
    def get_message_data(file_path, target_id="0x1"):
        """
        Reads a text file and returns the message data for the specified target ID.
        """
        with open(file_path, 'r') as file:
            for line in file:
                components = line.strip().split(', ')
                if len(components) < 4:
                    continue 

                # Check if this line contains the target protocol
                if target_id in line:
                    # Extract the protocol part and check if it matches
                    protocol_part = components[2].strip()
                    if target_id in protocol_part:
                        message_data = components[-1]
                        return message_data.strip()

        return None

    @staticmethod
    def count_protocols_in_data(file_path):
        protocol_counts = {}
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    if '0x' in line:
                        parts = line.split(', ')
                        if len(parts) >= 3:
                            protocol = parts[2]
                            if '0x' in protocol:
                                protocol_counts[protocol] = protocol_counts.get(protocol, 0) + 1
                                
        except FileNotFoundError:
            print(f"File {file_path} not found")
            return {}
        except Exception as e:
            print(f"Error reading file: {e}")
            return {}
        
        return protocol_counts


