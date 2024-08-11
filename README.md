# SymDFA2Aiger

## Description

SymDFA2Aiger is a tool for converting a symbolic deterministic finite automaton (SDFA) into an AIGER file (.aag). The main function provided is `SymDFA2Aiger`. 
An example input file is included in this directory to illustrate the expected format for the function.

### Personal Note

This tool was created by Daniel Bachmann Aisen as part of his master’s thesis. 
In 2024, amidst challenging times, this project is dedicated to the safe return of all hostages, to the soldiers safeguarding my friends, family, and me, and in memory of those who have fallen. 
May we look forward to better days.

## Inputs

The tool requires five inputs corresponding to SDFA properties:

- `sigma_controlled`: `set[Formula]`
- `sigma_environment`: `set[Formula]`
- `state_variables`: `set[Formula]`
- `initial_state`: `PLTLAnd`
- `transition_system`: `dict`

### Optional Inputs

- `file_name`: `str` (default: `"SymbDFA_AIGER.aag"`)
- `state_variables_return_dict`: `dict` (default: `None`)

### Example Usage

```python
a = parse_pltl("a")
b = parse_pltl("b")
c = parse_pltl("c")
d = parse_pltl("d")
_x1 = parse_pltl("x_var1")
_x2 = parse_pltl("x_var2")
_x3 = parse_pltl("x_var3")
_x4 = parse_pltl("x_var4")

sigma_controlled = {a, c}
sigma_environment = {b, d}

initial_state_input = PLTLAnd(_x1, PLTLNot(_x2), _x3, _x4)
final_state_variable = PLTLAnd(_x1, _x2, PLTLNot(_x3), PLTLNot(_x4))
state_variables_input = [_x1, _x2, _x3, _x4]

transition_system_input = {}
transition_system_input["x_var1_prime"] = parse_pltl("a")
transition_system_input["x_var2_prime"] = parse_pltl("b")
transition_system_input["x_var3_prime"] = parse_pltl("(false|a|(b&d)|!c)")
transition_system_input["x_var4_prime"] = parse_pltl(" ((! a) & ! c )")

SymDFA2AIGER(sigma_controlled, sigma_environment, state_variables_input, initial_state_input, transition_system_input, final_state_variable, "experiment_aiger.aag")
```


## Installation and Dependencies

This tool requires two external libraries: [pylogics_modalities](https://github.com/danielaisen/pylogics_modalities) and `multipledispatch`.

- **pylogics_modalities**: This library extends the pylogics library by whitemech. To install it, use the `.whl` file provided in the `dependencies` folder:

`pip install dependencies/pylogics_modalities-0.2.2-py3-none-any.whl`

```bash
pip install SymDFA2Aiger