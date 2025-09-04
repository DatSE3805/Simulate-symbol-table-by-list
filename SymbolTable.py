from StaticError import *
from Symbol import *
from functools import *

def check_valid_identifier(name):
    return (name[0].islower() and 
            all(c.isalnum() or c == '_' for c in name))

def check_valid_type(typ):
    return typ in ["number", "string"]

def check_valid_value(value, cmd):
    if value.isdigit():
        return ("number", value)
    elif (len(value) >= 2 and value[0] == "'" and value[-1] == "'"):
        content = value[1:-1]
        if not all(c.isalnum() for c in content):
            raise InvalidInstruction(cmd)
        return ("string", content)
    return None

def lookup_symbol_recursive(name, scope_data):
    symbols, level, parent = scope_data
    found = next((sym for sym in symbols if sym.name == name), None)
    return ((found, level) if found else 
            lookup_symbol_recursive(name, parent) if parent is not None else 
            (None, None))

def collect_symbols_forward(scope_data, seen_names=frozenset()):
    symbols, level, parent = scope_data
    current_symbols = [(sym.name, level) 
                      for sym in symbols 
                      if sym.name not in seen_names]
    updated_seen = frozenset([sym.name for sym in symbols]).union(seen_names)
    parent_symbols = ([] if parent is None 
                     else collect_symbols_forward(parent, updated_seen))
    return parent_symbols + current_symbols

def collect_symbols_reverse(scope_data, seen_names=frozenset()):
    symbols, level, parent = scope_data
    current_symbols = [(sym.name, level) 
                      for sym in reversed(symbols)
                      if sym.name not in seen_names]
    updated_seen = frozenset([sym.name for sym in symbols]).union(seen_names)
    parent_symbols = ([] if parent is None 
                     else collect_symbols_reverse(parent, updated_seen))
    return current_symbols + parent_symbols

def process_command(cmd, scope_stack):
    def handle_insert(cmd, parts, current_scope):
        if len(parts) != 3 or len(cmd.split(None, 2)) != 3:
            raise InvalidInstruction(cmd)
        if cmd != f"INSERT {parts[1]} {parts[2]}":
            raise InvalidInstruction(cmd)
        
        name, typ = parts[1:]
        
        if name[0].isupper() or name[0] == '_' or name[0].isdigit() or '@' in name or '`' in name or '~' in name:
            raise InvalidInstruction(cmd)
        if not check_valid_identifier(name):
            raise InvalidInstruction(cmd)
        if not check_valid_type(typ):
            raise InvalidInstruction(cmd)
        symbols, level, parent = current_scope
        if any(sym.name == name for sym in symbols):
            raise Redeclared(cmd)
            
        return ("success",
                tuple(list(scope_stack[:-1]) +
                     [(tuple(list(symbols) + [Symbol(name, typ)]), level, parent)]))

    def handle_assign(cmd, parts, current_scope):
        if len(parts) != 3 or len(cmd.split(None, 2)) != 3:
            raise InvalidInstruction(cmd)
        if cmd != f"ASSIGN {parts[1]} {parts[2]}":
            raise InvalidInstruction(cmd)
            
        name, value = parts[1:]
        
        if name[0].isupper() or name[0] == '_' or name[0].isdigit() or '@' in name or '`' in name or '~' in name:
            raise InvalidInstruction(cmd)
        if not check_valid_identifier(name):
            raise InvalidInstruction(cmd)
        target_sym, _ = lookup_symbol_recursive(name, current_scope)
        if not target_sym:
            raise Undeclared(cmd)

        try:
            value_info = check_valid_value(value, cmd)
            if value_info:
                value_type, value_content = value_info
                if value_type != target_sym.typ:
                    raise TypeMismatch(cmd)
            else:
                if not check_valid_identifier(value):
                    raise InvalidInstruction(cmd)
                value_sym, _ = lookup_symbol_recursive(value, current_scope)
                if not value_sym:
                    raise Undeclared(cmd)
                if value_sym.typ != target_sym.typ:
                    raise TypeMismatch(cmd)
        except InvalidInstruction as e:
            raise InvalidInstruction(cmd)
                
        return ("success", scope_stack)

    def handle_begin(cmd, parts, current_scope):
        if len(parts) != 1 or cmd != "BEGIN":
            raise InvalidInstruction(cmd)
        return (None, tuple(list(scope_stack) +
                           [((), current_scope[1] + 1, current_scope)]))

    def handle_end(cmd, parts, _):
        if len(parts) != 1 or cmd != "END":
            raise InvalidInstruction(cmd)
        if len(scope_stack) <= 1:
            raise UnknownBlock()
        return (None, scope_stack[:-1])

    def handle_lookup(cmd, parts, current_scope):
        if len(parts) != 2 or len(cmd.split(None, 1)) != 2:
            raise InvalidInstruction(cmd)
        if cmd != f"LOOKUP {parts[1]}":
            raise InvalidInstruction(cmd)
        name = parts[1]
        if name[0].isupper() or name[0] == '_' or name[0].isdigit() or '@' in name or '`' in name or '~' in name:
            raise InvalidInstruction(cmd)
        if not check_valid_identifier(name):
            raise InvalidInstruction(cmd)
        _, level = lookup_symbol_recursive(name, current_scope)
        if level is None:
            raise Undeclared(cmd)
        return (str(level), scope_stack)

    def handle_print(cmd, parts, current_scope):
        if len(parts) != 1 or cmd != "PRINT":
            raise InvalidInstruction(cmd)
        return (("", scope_stack) if not collect_symbols_forward(current_scope) else
                (" ".join(f"{name}//{level}"
                         for name, level in collect_symbols_forward(current_scope)),
                 scope_stack))

    def handle_rprint(cmd, parts, current_scope):
        if len(parts) != 1 or cmd != "RPRINT":
            raise InvalidInstruction(cmd)
        return (("", scope_stack) if not collect_symbols_reverse(current_scope) else
                (" ".join(f"{name}//{level}"
                         for name, level in collect_symbols_reverse(current_scope)),
                 scope_stack))

    handlers = {
        "INSERT": handle_insert,
        "ASSIGN": handle_assign,
        "BEGIN": handle_begin,
        "END": handle_end,
        "LOOKUP": handle_lookup,
        "PRINT": handle_print,
        "RPRINT": handle_rprint
    }
    if not cmd:
        raise InvalidInstruction("Invalid command")
    if cmd[0].isspace():
        raise InvalidInstruction("Invalid command")
    parts = cmd.split()
    if not parts:
        raise InvalidInstruction("Invalid command")
    if parts[0] not in handlers:
        raise InvalidInstruction("Invalid command")
    if len(cmd.split()) != len(cmd.split(None)):
        raise InvalidInstruction(cmd)

    return handlers[parts[0]](cmd, parts, scope_stack[-1])

def simulate(list_of_commands):
    def process_commands(commands, stack):
        if not commands:
            if len(stack) <= 1:
                return []
            raise UnclosedBlock(str(stack[-1][1]))
        try:
            result, new_stack = process_command(commands[0], stack)
            next_results = process_commands(commands[1:], new_stack)
            return ([result] if result is not None else []) + next_results
        except UnclosedBlock as e:
            raise e

    return process_commands(list_of_commands, (((), 0, None),))
