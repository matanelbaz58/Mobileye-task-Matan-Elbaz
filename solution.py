from typing import List


class Solution:
    def __init__(self, data_file_path: str, protocol_json_path: str):
        self.data_file_path = data_file_path
        self.protocol_json_path = protocol_json_path

    # Question 1: What is the version name used in the communication session?
    def q1(self) -> str:
        pass

    # Question 2: Which protocols have wrong messages frequency in the session compared to their expected frequency based on FPS?
    def q2(self) -> List[str]:
        pass

    # Question 3: Which protocols are listed as relevant for the version but are missing in the data file?
    def q3(self) -> List[str]:
        pass

    # Question 4: Which protocols appear in the data file but are not listed as relevant for the version?
    def q4(self) -> List[str]:
        pass

    # Question 5: Which protocols have at least one message in the session with mismatch between the expected size integer and the actual message content size?
    def q5(self) -> List[str]:
        pass

    # Question 6: Which protocols are marked as non dynamic_size in protocol.json, but appear with inconsistent expected message sizes Integer in the data file?
    def q6(self) -> List[str]:
        pass
