MAX_PARAMETERS = 3


def get_program(file_path):
    with open(file_path) as f:
        program = [int(e) for e in f.readline().split(',')]
    return program


def run_program(program):
    opcode_handlers = {1: _add,
                       2: _multiply,
                       5: _jump_if_true,
                       6: _jump_if_false,
                       7: _less_than,
                       8: _equals}
    pc = 0
    while 0 <= pc < len(program):
        instruction = program[pc]
        opcode, parameter_modes = _parse_instruction(instruction)
        if opcode == 99:  # Halt.
            break
        elif opcode == 3:  # Input.
            value = yield
            pc = _store(pc, program, value)
        elif opcode == 4:  # Output.
            pc, output = _disp(pc, program, parameter_modes)
            yield output
        else:
            try:
                pc = opcode_handlers[opcode](pc, program, parameter_modes)
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


def _store(pc, program, value):
    ret = program[pc + 1]
    program[ret] = value
    return pc + 2


def _disp(pc, program, parameter_modes):
    op = _get_parameter(program[pc + 1], parameter_modes[0], program)
    return pc + 2, op


def _add(pc, program, parameter_modes):
    op1 = _get_parameter(program[pc + 1], parameter_modes[0], program)
    op2 = _get_parameter(program[pc + 2], parameter_modes[1], program)
    ret = program[pc + 3]
    program[ret] = op1 + op2
    return pc + 4


def _multiply(pc, program, parameter_modes):
    op1 = _get_parameter(program[pc + 1], parameter_modes[0], program)
    op2 = _get_parameter(program[pc + 2], parameter_modes[1], program)
    ret = program[pc + 3]
    program[ret] = op1 * op2
    return pc + 4


def _jump_if_true(pc, program, parameter_modes):
    op1 = _get_parameter(program[pc + 1], parameter_modes[0], program)
    op2 = _get_parameter(program[pc + 2], parameter_modes[1], program)
    return op2 if op1 else pc + 3


def _jump_if_false(pc, program, parameter_modes):
    op1 = _get_parameter(program[pc + 1], parameter_modes[0], program)
    op2 = _get_parameter(program[pc + 2], parameter_modes[1], program)
    return pc + 3 if op1 else op2


def _less_than(pc, program, parameter_modes):
    op1 = _get_parameter(program[pc + 1], parameter_modes[0], program)
    op2 = _get_parameter(program[pc + 2], parameter_modes[1], program)
    ret = program[pc + 3]
    program[ret] = 1 if op1 < op2 else 0
    return pc + 4


def _equals(pc, program, parameter_modes):
    op1 = _get_parameter(program[pc + 1], parameter_modes[0], program)
    op2 = _get_parameter(program[pc + 2], parameter_modes[1], program)
    ret = program[pc + 3]
    program[ret] = 1 if op1 == op2 else 0
    return pc + 4


def _get_parameter(parameter, mode, program):
    if mode == 0:
        return program[parameter]
    elif mode == 1:
        return parameter
    else:
        print("ERROR: Invalid parameter mode: {}".format(mode))
