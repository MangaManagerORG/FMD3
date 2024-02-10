import enum


class DLDChaptersStatus(enum.Enum):
    NOT_DOWNLOADED = 0
    DOWNLOADED = 1  # Chapter completed
    ADDED_TO_QUEUE = 2  # added to queue. (If program exists these will be loaded first on next scan)
    SKIPPED = 3  # (file existing and apparently correct)
    ERRORED = 4  # Chapter downloads that errored. #Todo: reload them in tasks (maybe on next scan? add retry counter?)

    def as_name(self):
        return self.name.replace("_", " ")