import collections as coll


MAX_PARAMETERS = 3


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
        if opcode == 99:  # Halt.
            break
        elif opcode == 3:  # Input.
            value = yield
            pc = _store(pc, program, parameter_modes, relative_base, value)
        elif opcode == 4:  # Output.
            pc, output = _disp(pc, program, parameter_modes, relative_base)
            yield output
        elif opcode == 9:  # Adjust relative base.
            pc, relative_base = _adjust_relative_base(pc, program, parameter_modes, relative_base)
        else:
            try:
                pc = opcode_handlers[opcode](pc, program, parameter_modes, relative_base)
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


def _store(pc, program, parameter_modes, relative_base, value):
    ret = _get_return_address(program[pc + 1], parameter_modes[0], program, relative_base)
    program[ret] = value
    return pc + 2


def _disp(pc, program, parameter_modes, relative_base):
    op = _get_parameter(program[pc + 1], parameter_modes[0], program, relative_base)
    return pc + 2, op


def _adjust_relative_base(pc, program, parameter_modes, relative_base):
    op = _get_parameter(program[pc + 1], parameter_modes[0], program, relative_base)
    return pc + 2, relative_base + op


def _add(pc, program, parameter_modes, relative_base):
    op1 = _get_parameter(program[pc + 1], parameter_modes[0], program, relative_base)
    op2 = _get_parameter(program[pc + 2], parameter_modes[1], program, relative_base)
    ret = _get_return_address(program[pc + 3], parameter_modes[2], program, relative_base)
    program[ret] = op1 + op2
    return pc + 4


def _multiply(pc, program, parameter_modes, relative_base):
    op1 = _get_parameter(program[pc + 1], parameter_modes[0], program, relative_base)
    op2 = _get_parameter(program[pc + 2], parameter_modes[1], program, relative_base)
    ret = _get_return_address(program[pc + 3], parameter_modes[2], program, relative_base)
    program[ret] = op1 * op2
    return pc + 4


def _jump_if_true(pc, program, parameter_modes, relative_base):
    op1 = _get_parameter(program[pc + 1], parameter_modes[0], program, relative_base)
    op2 = _get_parameter(program[pc + 2], parameter_modes[1], program, relative_base)
    return op2 if op1 else pc + 3


def _jump_if_false(pc, program, parameter_modes, relative_base):
    op1 = _get_parameter(program[pc + 1], parameter_modes[0], program, relative_base)
    op2 = _get_parameter(program[pc + 2], parameter_modes[1], program, relative_base)
    return pc + 3 if op1 else op2


def _less_than(pc, program, parameter_modes, relative_base):
    op1 = _get_parameter(program[pc + 1], parameter_modes[0], program, relative_base)
    op2 = _get_parameter(program[pc + 2], parameter_modes[1], program, relative_base)
    ret = _get_return_address(program[pc + 3], parameter_modes[2], program, relative_base)
    program[ret] = 1 if op1 < op2 else 0
    return pc + 4


def _equals(pc, program, parameter_modes, relative_base):
    op1 = _get_parameter(program[pc + 1], parameter_modes[0], program, relative_base)
    op2 = _get_parameter(program[pc + 2], parameter_modes[1], program, relative_base)
    ret = _get_return_address(program[pc + 3], parameter_modes[2], program, relative_base)
    program[ret] = 1 if op1 == op2 else 0
    return pc + 4


def _get_parameter(parameter, mode, program, relative_base):
    if mode == 0:
        return program[parameter]
    elif mode == 1:
        return parameter
    elif mode == 2:
        return program[parameter + relative_base]
    else:
        print("ERROR: Invalid parameter mode: {}".format(mode))


def _get_return_address(parameter, mode, program, relative_base):
    if mode == 0:
        return parameter
    elif mode == 2:
        return parameter + relative_base
    else:
        print("ERROR: Invalid parameter mode for return address: {}".format(mode))
