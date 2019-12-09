import collections as coll


MAX_PARAMETERS = 3


class IntcodeSegmentationFault(Exception):
    pass


class Memory(list):
    def __init__(self, content):
        list.__init__(self, content)

    def __getitem__(self, key):
        try:
            return list.__getitem__(self, key)
        except IndexError:
            raise IntcodeSegmentationFault("Invalid read access at {} [0-{}]".format(key, len(self) - 1))

    def __setitem__(self, key, value):
        try:
            list.__setitem__(self, key, value)
        except IndexError:
            raise IntcodeSegmentationFault("Invalid write access at {} [0-{}]".format(key, len(self) - 1))


def get_program(file_path):
    memory = coll.defaultdict(int)
    with open(file_path) as f:
        program = [int(e) for e in f.readline().split(',')]
    memory.update({i: e for i, e in enumerate(program)})
    return memory


def run_program(program):
    opcode_handlers = {1: _add,
                       2: _multiply,
                       5: _jump_if_true,
                       6: _jump_if_false,
                       7: _less_than,
                       8: _equals}
    relative_base = 0
    pc = 0
    while 0 <= pc < len(program):
        instruction = program[pc]
        opcode, parameter_modes = _parse_instruction(instruction)
        parameter_provider = _get_parameter_provider(pc, program, parameter_modes, relative_base)
        return_value_handler = _get_return_value_handler(pc, program, parameter_modes, relative_base)
        if opcode == 99:  # Halt.
            break
        elif opcode == 3:  # Input.
            value = yield
            pc = _store(pc, return_value_handler, value)
        elif opcode == 4:  # Output.
            pc, output = _disp(pc, parameter_provider)
            yield output
        elif opcode == 9:  # Adjust relative base.
            pc, relative_base = _adjust_relative_base(pc, parameter_provider, relative_base)
        else:
            try:
                pc = opcode_handlers[opcode](pc, parameter_provider, return_value_handler)
            except KeyError:
                print("ERROR: Invalid opcode: {}".format(opcode))
                break
    else:
        print("ERROR: Invalid pc at {}".format(pc))


def _parse_instruction(instruction):
    instruction = str(instruction)
    opcode = int(''.join(instruction[-2:]))
    parameter_modes = [int(d) for d in reversed(instruction[:-2])]
    parameter_modes = parameter_modes + [0] * (MAX_PARAMETERS - len(parameter_modes))
    return opcode, parameter_modes


def _get_parameter_provider(pc, program, parameter_modes, relative_base):
    def _get_parameter(parameter, mode):
        if mode == 0:
            return program[parameter]
        elif mode == 1:
            return parameter
        elif mode == 2:
            return program[parameter + relative_base]
        else:
            print("ERROR: Invalid parameter mode: {}".format(mode))

    return lambda offset: _get_parameter(program[pc + 1 + offset], parameter_modes[offset])


def _get_return_value_handler(pc, program, parameter_modes, relative_base):
    def _get_return_address(parameter, mode):
        if mode == 0:
            return parameter
        elif mode == 2:
            return parameter + relative_base
        else:
            print("ERROR: Invalid return address parameter mode: {}".format(mode))

    def _store_return_value(offset, value):
        # PC position should be the current instruction.
        address = _get_return_address(program[pc + 1 + offset], parameter_modes[offset])
        program[address] = value

    return _store_return_value


def _store(pc, return_value_handler, value):
    return_value_handler(0, value)
    return pc + 2


def _disp(pc, parameter_provider):
    op = parameter_provider(0)
    return pc + 2, op


def _adjust_relative_base(pc, parameter_provider, relative_base):
    op = parameter_provider(0)
    return pc + 2, relative_base + op


def _add(pc, parameter_provider, return_value_handler):
    op1 = parameter_provider(0)
    op2 = parameter_provider(1)
    return_value_handler(2, op1 + op2)
    return pc + 4


def _multiply(pc, parameter_provider, return_value_handler):
    op1 = parameter_provider(0)
    op2 = parameter_provider(1)
    return_value_handler(2, op1 * op2)
    return pc + 4


def _jump_if_true(pc, parameter_provider, return_value_handler):
    op1 = parameter_provider(0)
    op2 = parameter_provider(1)
    return op2 if op1 else pc + 3


def _jump_if_false(pc, parameter_provider, return_value_handler):
    op1 = parameter_provider(0)
    op2 = parameter_provider(1)
    return pc + 3 if op1 else op2


def _less_than(pc, parameter_provider, return_value_handler):
    op1 = parameter_provider(0)
    op2 = parameter_provider(1)
    return_value_handler(2, 1 if op1 < op2 else 0)
    return pc + 4


def _equals(pc, parameter_provider, return_value_handler):
    op1 = parameter_provider(0)
    op2 = parameter_provider(1)
    return_value_handler(2, 1 if op1 == op2 else 0)
    return pc + 4
