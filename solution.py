import json
from typing import List


class Solution:
    def __init__(self, data_file_path: str, protocol_json_path: str):
        self.data_file_path = data_file_path
        self.protocol_json_path = protocol_json_path

    # Question 1: What is the version name used in the communication session?
    def q1(self) -> str:
        with open(self.data_file_path, 'r') as f:
            first_line = f.readline().strip()
            if first_line:
                parts = first_line.split(',')
                if len(parts) >= 5:
                    message_data_hex = parts[4].strip().replace(' ', '')
                    return bytes.fromhex(message_data_hex).decode('ascii')
        return ""

    # Helper: Gets the 'relevant' protocol IDs for the session version from protocol.json
    def _get_relevant_pids(self) -> set:
        with open(self.protocol_json_path, 'r') as f:
            proto_info = json.load(f)
            
        version = self.q1()
            
        relevant_pids = set()
        try:
            v_info = proto_info['protocols_by_version'][version]
            p_list = v_info.get('protocols', [])
            id_type = v_info.get('id_type', 'hex')
            for p in p_list:
                if id_type == 'dec':
                    relevant_pids.add(hex(int(p)))
                else:
                    relevant_pids.add(p)
        except KeyError:
            raise KeyError(f"Version '{version}' not found in {self.protocol_json_path}")
        return relevant_pids

    # Helper: Gets all observed protocol IDs and their occurrence counts from data.txt
    def _get_observed_pids_counts(self) -> dict:
        counts = {}
        with open(self.data_file_path, 'r') as f:
            for line in f:
                parts = line.split(',')
                if len(parts) >= 3:
                    pid = parts[2].strip()
                    counts[pid] = counts.get(pid, 0) + 1
        return counts

    # Question 2: Which protocols have wrong messages frequency in the session compared to their expected frequency based on FPS?
    def q2(self) -> List[str]:
        with open(self.protocol_json_path, 'r') as f:
            proto_info = json.load(f)
            
        relevant_pids = self._get_relevant_pids()
        counts = self._get_observed_pids_counts()
                
        expected_freq = {
            36: 164,
            18: 84,
            9: 48,
            1: 1
        }
        
        all_pids_to_check = relevant_pids.union(counts.keys())
        wrong_freq_protocols = set()
        
        for pid in all_pids_to_check:
            count = counts.get(pid, 0)
            if pid in proto_info.get('protocols', {}):
                fps = proto_info['protocols'][pid].get('fps')
                if fps in expected_freq:
                    if count != expected_freq[fps]:
                        wrong_freq_protocols.add(pid)
                        
        return list(wrong_freq_protocols)

    # Question 3: Which protocols are listed as relevant for the version but are missing in the data file?
    def q3(self) -> List[str]:
        relevant_pids = self._get_relevant_pids()
        observed_pids = set(self._get_observed_pids_counts().keys())
                    
        missing_pids = relevant_pids - observed_pids
        return list(missing_pids)

    # Question 4: Which protocols appear in the data file but are not listed as relevant for the version?
    def q4(self) -> List[str]:
        relevant_pids = self._get_relevant_pids()
        observed_pids = set(self._get_observed_pids_counts().keys())
                    
        unexpected_pids = observed_pids - relevant_pids
        return list(unexpected_pids)

    # Question 5: Which protocols have at least one message in the session with mismatch between the expected size integer and the actual message content size?
    def q5(self) -> List[str]:
        mismatch_pids = set()
        with open(self.data_file_path, 'r') as f:
            for line in f:
                parts = line.split(',')
                if len(parts) >= 5:
                    pid = parts[2].strip()
                    try:
                        # Extract the expected size number (e.g. "8    bytes")
                        expected_size_str = parts[3].lower().replace('bytes', '').strip()
                        expected_size = int(expected_size_str)
                        
                        # Calculate the actual size by counting the hex tokens
                        # parts[4] contains the hex payload, e.g. " 56 65 72 ... "
                        actual_size = len(parts[4].strip().split())
                        
                        if expected_size != actual_size:
                            mismatch_pids.add(pid)
                    except ValueError:
                        pass
        return list(mismatch_pids)

    # Question 6: Which protocols are marked as non dynamic_size in protocol.json, but appear with inconsistent expected message sizes Integer in the data file?
    def q6(self) -> List[str]:
        with open(self.protocol_json_path, 'r') as f:
            proto_info = json.load(f)
            
        non_dynamic_pids = set()
        for pid, info in proto_info.get('protocols', {}).items():
            if info.get('dynamic_size') is False:
                non_dynamic_pids.add(pid)
                
        pid_to_sizes = {}
        with open(self.data_file_path, 'r') as f:
            for line in f:
                parts = line.split(',')
                if len(parts) >= 4:
                    pid = parts[2].strip()
                    if pid in non_dynamic_pids:
                        try:
                            # Extract the expected size number (e.g. "8    bytes")
                            expected_size_str = parts[3].lower().replace('bytes', '').strip()
                            expected_size = int(expected_size_str)
                            
                            if pid not in pid_to_sizes:
                                pid_to_sizes[pid] = set()
                            pid_to_sizes[pid].add(expected_size)
                        except ValueError:
                            pass
                            
        inconsistent_pids = [pid for pid, sizes in pid_to_sizes.items() if len(sizes) > 1]
        return inconsistent_pids


if __name__ == "__main__":
    solution = Solution("data.txt", "protocol.json")
    print("Q1:", solution.q1())
    print("Q2:", solution.q2())
    print("Q3:", solution.q3())
    print("Q4:", solution.q4())
    print("Q5:", solution.q5())
    print("Q6:", solution.q6())
