from pydantic import RootModel

class PlayTimeGenre_(RootModel):
  root: dict
  def __getitem__(self, item):
    return getattr(self, item)