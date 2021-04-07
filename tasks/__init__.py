from invoke import Collection

from tasks import lint, reformat

namespace = Collection(lint, reformat)
