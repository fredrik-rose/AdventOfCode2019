# Day 23: Category Six
import os
import sys
import threading
import time

import queue

sys.path.append(os.path.join(sys.path[0], '..', 'intcodecomputer'))
import intcodecomputer as intcom


NUMBER_OF_COMPUTERS = 50
NAT_ADDRESS = 255
EMPTY_QUEUE = -1


def create_network(program, stop_event):
    queues = {i: queue.Queue() for i in range(NUMBER_OF_COMPUTERS)}
    queues[NAT_ADDRESS] = queue.LifoQueue()  # Luckily works also for part one (should really be a FIFO queue).
    threads = [threading.Thread(target=nic_thread, args=(queues, program.copy(), address, stop_event))
               for address in queues.keys()]
    return queues, threads


def nic_thread(queues, program, my_address, stop_event):
    computer = intcom.run_program(program.copy(), input_provider(queues, my_address, stop_event))
    while True:
        try:
            address, x, y = create_packet(computer)
        except StopIteration:
            break
        print("Sending packet ({}, {}) from {} to {}".format(x, y, my_address, address), flush=True)
        queues[address].put((x, y))


def input_provider(queues, my_address, stop_event):
    def input_generator():
        yield my_address  # The program expects the first input value to be the address.
        while not stop_event.isSet():
            try:
                packet = queues[my_address].get(block=False)
                for element in packet:
                    yield element
            except queue.Empty:
                time.sleep(0.0001)  # Yield control to other threads.
                yield EMPTY_QUEUE

    def provider():
        return next(generator)

    generator = input_generator()
    return provider


def create_packet(computer):
    address = next(computer)
    x = next(computer)
    y = next(computer)
    return address, x, y


def nat_thread(queues, my_address):
    previous_y_value = None
    while True:
        empty_queue_counter = 0
        while all(qeueu.empty() for address, qeueu in queues.items() if address != my_address):
            time.sleep(0.0001)  # Yield control to other threads.
            empty_queue_counter += 1
            if empty_queue_counter > 10:
                # The queues have been empty for several consecutive iteration, thus the network is idle.
                x, y = queues[my_address].get()
                print("Network is idle, sending packet ({}, {}) from NAT to 0".format(x, y), flush=True)
                queues[0].put((x, y))
                if y == previous_y_value:
                    return y
                previous_y_value = y
        time.sleep(0.1)  # Yield control to other threads.


def part_one(program):
    stop_event = threading.Event()
    queues, threads = create_network(program, stop_event)
    for thread in threads:
        thread.start()
    _, y = queues[NAT_ADDRESS].get(block=True)
    stop_event.set()
    for thread in threads:
        thread.join()
    print("Y value of the first packet sent to address {}: {}".format(NAT_ADDRESS, y), flush=True)


def part_two(program):
    stop_event = threading.Event()
    queues, threads = create_network(program, stop_event)
    for thread in threads:
        thread.start()
    y = nat_thread(queues, NAT_ADDRESS)
    stop_event.set()
    for thread in threads:
        thread.join()
    print("The first Y value delivered by the NAT to the computer at address 0 twice in a row: {}".format(y),
          flush=True)


def main():
    program = intcom.get_program('23.txt')
    part_one(program.copy())
    input("Pres any key to continue with part two...")
    part_two(program.copy())


if __name__ == "__main__":
    main()
