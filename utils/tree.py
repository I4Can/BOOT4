
def preorder(root):
    if not root:
        return []
    if not root.answer.first():
        return [root]
    result = [root]
    for child in root.answer.all():
        result += preorder(child)
    return result
