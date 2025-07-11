def print_error(err_type, custom_msg, msg=None):
    print("---------------\n"
          f"{err_type}: {custom_msg}.\n"
          f"{"Mensagem: " + str(msg) + "\n" if msg else ""}"
          "---------------")
