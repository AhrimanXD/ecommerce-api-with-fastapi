

def exists(session, entity, pk):
  obj = session.get(entity, pk)
  if not obj:
    return False
  return True