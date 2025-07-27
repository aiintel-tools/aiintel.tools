"""
Gunicorn configuration for the AI Directory Platform.
"""

import multiprocessing

# Bind to 0.0.0.0:5000
bind = "0.0.0.0:5000"

# Number of worker processes
workers = multiprocessing.cpu_count() * 2 + 1

# Worker class
worker_class = "sync"

# Timeout in seconds
timeout = 120

# Log level
loglevel = "info"

# Access log format
accesslog = "-"

# Error log
errorlog = "-"

# Preload application
preload_app = True

# Maximum number of requests a worker will process before restarting
max_requests = 1000
max_requests_jitter = 50

