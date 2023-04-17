def log(log_stream, message):
        log_stream.write(message + '\n')
        log_stream.flush()
        print(message)
