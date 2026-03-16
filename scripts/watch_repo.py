from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
from workflows.autonomous_dev_loop import run_loop


class RepoWatcher(FileSystemEventHandler):

    def __init__(self, repo_path):
        self.repo_path = repo_path

    def on_modified(self, event):

        print("Repo changed. Running agent...")

        run_loop(self.repo_path)


def watch(repo_path):

    observer = Observer()

    handler = RepoWatcher(repo_path)

    observer.schedule(handler, repo_path, recursive=True)

    observer.start()

    try:
        while True:
            time.sleep(5)

    except KeyboardInterrupt:
        observer.stop()

    observer.join()