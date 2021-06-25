import logging
import zipfile
import sys
from datetime import datetime
from multiprocessing import Process
from time import sleep

compression = zipfile.ZIP_DEFLATED

filename = datetime.now().strftime("%Y-%m-%d_%H:%M:%S") + '.log'
# filename = 'test_file.log'


logger = logging.getLogger()
logger.setLevel(logging.INFO)

output_handler = logging.FileHandler(filename)
stdout_handler = logging.StreamHandler(sys.stdout)

logger.addHandler(output_handler)
logger.addHandler(stdout_handler)

# logging.basicConfig(format='%(levelname)s:%(message)s', filename=filename, level=logging.INFO)


def log_file() -> None:
    count = 0
    sleep(1)
    while True:
        logger.info(datetime.now().strftime("%Y-%m-%d %H:%M:%S - ") +
                    "this is log number %d", count)

        if count > 0 and count % 30 == 0:
            f = open(filename, 'r+')
            f.truncate(0)
            zipObj = zipfile.ZipFile('log_archive/' + datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + '.zip', 'w')
            zipObj.write(filename)
            zipObj.close
        count += 1
        sleep(1)


log_process = Process(target=log_file, name="Process_inc_forever")
log_process.start()
log_process.join(timeout=120)
log_process.terminate()

if log_process.exitcode is None:
    logger.info("process terminated after 120 seconds")
