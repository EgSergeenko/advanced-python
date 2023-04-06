import codecs
import os
import time
from datetime import datetime
from multiprocessing import Lock, Pipe, Process, Queue
from multiprocessing.connection import Connection

QUIT_COMMAND = 'quit'
log_file_lock = Lock()


def log_to_file(message: str, message_time: datetime) -> None:
    with log_file_lock:
        with open('artifacts/hard.txt', 'a') as log_file:
            log_file.write(
                '{0}, PID={1}, time={2}\n'.format(
                    message,
                    os.getpid(),
                    message_time,
                ),
            )


def a_worker(conn: Connection, q: Queue) -> None:
    while True:
        command = conn.recv()
        log_to_file(
            'Received command: {0}'.format(command),
            datetime.now(),
        )
        if command == QUIT_COMMAND:
            log_to_file('Quitting', datetime.now())
            conn.close()
            q.put(command)
            break
        q.put(command.lower())
        log_to_file(
            'Put command: {0}'.format(command),
            datetime.now(),
        )
        time.sleep(5)


def b_worker(conn: Connection, q: Queue) -> None:
    while True:
        command = q.get()
        log_to_file(
            'Got command: {0}'.format(command),
            datetime.now(),
        )
        if command == QUIT_COMMAND:
            log_to_file('Quitting', datetime.now())
            conn.close()
            break
        encoded_command = codecs.encode(command, 'rot_13')
        conn.send(encoded_command)
        log_to_file(
            'Sent command: {0}'.format(encoded_command),
            datetime.now(),
        )


def main() -> None:
    parent_conn_a, child_conn_a = Pipe()
    parent_conn_b, child_conn_b = Pipe()
    q: Queue = Queue()

    a = Process(target=a_worker, args=(child_conn_a, q))
    b = Process(target=b_worker, args=(child_conn_b, q))

    a.start()
    b.start()

    while True:
        command = input()
        log_to_file(
            'Input: {0}'.format(command),
            datetime.now(),
        )
        parent_conn_a.send(command)
        if command == QUIT_COMMAND:
            log_to_file('Quitting', datetime.now())
            a.join()
            b.join()
            parent_conn_a.close()
            parent_conn_b.close()
            break
        encoded_command = parent_conn_b.recv()
        log_to_file(
            'Output: {0}'.format(encoded_command),
            datetime.now(),
        )


if __name__ == '__main__':
    main()
