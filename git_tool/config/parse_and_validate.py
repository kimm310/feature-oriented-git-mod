Config = str  # TODO represent the schema of a configuration


def parse_configuration_file(filename) -> Config: ...


def validate_configuration(config: Config) -> bool:
    return False
