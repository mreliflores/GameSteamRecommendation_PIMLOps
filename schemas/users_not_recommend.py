from pydantic import root_model

class UsersNotRecommend_(root_model):
  root: dict
  def __getitem__(self, item):
    return getattr(self, item)