from radar.lib import get_repo_path
from git import Repo
import git.exc
import os.path


def clone_or_update_repo(url=None, repo_name=None):
    '''
    Clone a repo to the path provided
    '''
    if not url:
        raise Exception('No URL provided')
    if not repo_name:
        raise Exception('No repo_name provided')

    path = os.path.join(get_repo_path(), repo_name)
    # Check if there's an existing clone
    try:
        repo = Repo(path)
    except git.exc.NoSuchPathError:
        repo = None

    if not repo:
        repo = Repo.clone_from(url, path)
        if not repo:
            raise Exception('Could not clone the repository')
        return repo

    repo.remote.pull()
    return repo
