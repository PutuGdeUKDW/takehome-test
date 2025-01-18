import os
import re
from datetime import datetime, timedelta
from file_read_backwards import FileReadBackwards


def logReader(directory):
    log_pattern = r'(\d+\.\d+\.\d+\.\d+) \S+ \S+ \[(.*?)\] ".*" (\d+)'
    log_file_pattern = 'Http-\d+.log'

    #For testing purpose. Uncomment the first current_time if using the provided logs, uncomment the second current_time if using newer logs
    current_time = datetime.strptime('2022-10-10:14:03:45', '%Y-%m-%d:%H:%M:%S')
    #current_time = datetime.utcnow()

    time_limit = current_time - timedelta(minutes=10)
    print(time_limit)
    http_500_count = 0


    log_files_list = []
    for i in os.listdir(directory):
        if re.match(log_file_pattern, i):
            log_files_list.append(i)

    log_files_list.sort(reverse=True)

    for log_file in log_files_list:
        log_path = os.path.join(directory, log_file)

        with FileReadBackwards(log_path, encoding="utf-8") as f:
            for line in f:
                match = re.search(log_pattern, line)
                if match:
                    timestamp_str = match.group(2)
                    response_code = match.group(3)
                    
                    log_time = datetime.strptime(timestamp_str.split(' ')[0], '%d/%b/%Y:%H:%M:%S')

                    if log_time < time_limit:
                        return http_500_count
                    if response_code == '500' and log_time >= time_limit:
                        http_500_count += 1
                    print(line)

    return http_500_count




if __name__ == '__main__':
    directory = 'log/'
    total_error_count = logReader(directory)
    print(f'HTTP 500 errors in the last 10 minutes: {total_error_count}')
