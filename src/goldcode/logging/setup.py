import logging

def get_logger(
    name: str,
    logger: logging.Logger | None = None,
    log_path: str | None = None,
    level=logging.INFO,
) -> logging.Logger:

    if logger:
        return logger

    log = logging.getLogger(name)
    log.setLevel(level)

    if log.handlers:
        return log

    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s: %(message)s"
    )

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    log.addHandler(stream_handler)

    if log_path:
        file_handler = logging.FileHandler(log_path, mode="a", encoding="utf-8")
        file_handler.setFormatter(formatter)
        log.addHandler(file_handler)

    return log
