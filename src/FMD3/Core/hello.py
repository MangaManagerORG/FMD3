from FMD3.Core import logging
def hello():
    print("Hello World")
    logging.getLogger().info("Test")
    logging.getLogger().trace()