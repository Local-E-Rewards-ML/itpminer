def check_type(input, input_str: str, input_type: type):
    if not isinstance(input, input_type):
        raise Exception(
            f"{input_str} needs to be of type {input_type} but {input} is of type: {type(input)}")
