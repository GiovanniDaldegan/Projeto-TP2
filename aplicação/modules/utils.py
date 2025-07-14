def print_error(err_type, custom_msg, msg=None):
    print(f"---------------\n{err_type}: {custom_msg}.\n" + (f"Mensagem: {msg}\n" if msg else "") + "---------------")
