from whitenoise.storage import CompressedManifestStaticFilesStorage
from whitenoise.storage import MissingFileError

class CustomStaticFilesStorage(CompressedManifestStaticFilesStorage):
    def post_process(self, paths, dry_run=False, **options):
        try:
            return super().post_process(paths, dry_run, **options)
        except MissingFileError:
            pass
        return []