from .sql_memory import build_memory
from .window_memory import window_buffer_memory_builder
from functools import partial

memory_map = {
    "sql_buffer_memory": build_memory,
    "sql_window_memory": window_buffer_memory_builder
}