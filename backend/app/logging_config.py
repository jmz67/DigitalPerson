
import logging
import sys

def setup_logging():
    # 获取名为 "uvicorn.access" 的日志记录器，这是 Uvicorn 用来记录访问日志的默认日志记录器。
    logger = logging.getLogger("uvicorn.access")

    # 设置日志级别为 INFO。这意味着只有严重程度等于或高于 INFO 的消息会被处理。
    logger.setLevel(logging.INFO)

    # 创建一个流处理器 (StreamHandler)，它会将日志消息发送到标准输出（sys.stdout）。
    handler = logging.StreamHandler(sys.stdout)

    # 定义日志消息格式，包括时间戳、日志记录器名称、日志级别和消息内容。
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # 将上面定义的日志格式设置给处理器。
    handler.setFormatter(formatter)

    # 将处理器添加到日志记录器中，这样当有日志消息时，就会通过这个处理器输出。
    logger.addHandler(handler)

    # 配置应用自己的日志记录器，这里使用 "app" 作为名称。
    app_logger = logging.getLogger("app")

    # 设置应用日志记录器的日志级别为 INFO。
    app_logger.setLevel(logging.INFO)

    # 为应用创建一个新的流处理器，同样指向标准输出。
    app_handler = logging.StreamHandler(sys.stdout)

    # 使用与 uvicorn 日志相同的格式化程序来保持一致性。
    app_handler.setFormatter(formatter)

    # 将处理器添加到应用的日志记录器中。
    app_logger.addHandler(app_handler)

# 注意：在实际应用中，通常会在应用程序启动时调用 setup_logging() 来配置日志记录。
