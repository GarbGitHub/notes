import environ
env = environ.Env()
env.read_env()

GET_CONFIG = env('GET_CONFIG')
