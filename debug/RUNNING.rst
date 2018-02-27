Debug
-----
First install ``ipdb`` for easier debugging process::

    pip install ipdb

Now update the ``./debug/<module_name>_args.json`` file with your credentials and command arguments, then run::

    python -m ipdb ./library/<module_name>.py ./debug/<module_name>_args.json

