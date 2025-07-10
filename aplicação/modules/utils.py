def print_error(err_type, custom_msg, msg=None):
    print(f"---------------\n{err_type}: {custom_msg}.\n{"Mensagem: " + str(msg) + "\n" if msg else ""}---------------")
