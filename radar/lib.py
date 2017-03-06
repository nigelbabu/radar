import os.path
import radar


__all__ = ['get_repo_path']


def get_repo_path():
    path = os.path.abspath(radar.__file__)
    # /path/to/radar/radar/__init.pyc

    path = os.path.dirname(path)
    # /path/to/radar/radar

    path = os.path.dirname(path)
    # /path/to/radar/

    path = os.path.join(path, radar.app.config.get('GIT_REPO_PATH', ''))
    # /path/to/radar/<git_repos>

    return path
