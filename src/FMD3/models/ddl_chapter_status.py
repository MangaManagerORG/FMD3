import enum


class DLDChaptersStatus(enum.Enum):
    NOT_DOWNLOADED = 0
    DOWNLOADED = 1  # Chapter completed
    ADDED_TO_QUEUE_USER = 2  # added to queue. Task created by user (manual download)
    SKIPPED = 3  # (file existing and apparently correct)
    ERRORED = 4  # Chapter downloads that errored. #Todo: reload them in tasks (maybe on next scan? add retry counter?)
    ADDED_TO_QUEUE_SCANNER = 5
    def as_name(self):
        return self.name.replace("_", " ")