import time

def log(log_stream, message):
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        log_stream.write(current_time + " " + message + '\n')
        log_stream.flush()
        print(message)


