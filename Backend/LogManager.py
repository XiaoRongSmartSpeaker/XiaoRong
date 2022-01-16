from cmath import log
import logging
import sys
import requests
import schedule
import time
import threading
import json
import logger.logger as logger

# set up logger
try:
    import logger
    logger = logger.setup_applevel_logger(file_name='./log/smartspeaker.log')
except ModuleNotFoundError as e:
    print(e)
    import logging
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

server_url = 'http://140.122.185.210/log/'

def clear_log():
    # send_log_to_server()
    open('log/smartspeaker.log', 'w').close()
    logger.debug("Log file cleared")

def send_log_to_server():
    try:
        with open('log/smartspeaker.log', 'r') as f:
            # this is test only, not a real user_id
            log_data = {
                "status": f.read(),
                "user_id": "001"
            }
            response = requests.post(server_url, json.dumps(log_data))
        response.raise_for_status()
        logger.debug("Successfully sent log file to server")
    except requests.exceptions.HTTPError as errh:
        logger.error(errh)
    except requests.exceptions.ConnectionError as errc:
        logger.error(errc)
    except requests.exceptions.Timeout as errt:
        logger.error(errt)
    except requests.exceptions.RequestException as err:
        logger.error(err)

def log_operation():
    send_log_to_server()
    clear_log()

def run_continuously(interval=1):
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                schedule.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.setDaemon(True)
    continuous_thread.start()
    return cease_continuous_run

# Stop the background thread
def stop_log_manager():
    stop_run_continuously.set()
    logger.debug("Log manager has been stopped")

# Start the background thread (upon importing this module)
stop_run_continuously = run_continuously()

# for production, uncomment this line
schedule.every().hour.do(log_operation)

# for test only
# schedule.every(30).seconds.do(log_operation)

# for test only
if __name__ == '__main__':
    schedule.every(10).seconds.do(log_operation)
    for i in range(30):
        time.sleep(1)
        print("running ...")
        logger.debug("this is a message from LogManager")
    stop_run_continuously.set()