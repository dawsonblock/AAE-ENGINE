class BaseMutation:
    mutation_type = "base"

    def generate(self, tree, context=None):
        return []

class FlipConditionMutation(BaseMutation):
    mutation_type = "flip_condition"

    def generate(self, tree, context=None):
        return []

class AddNoneGuardMutation(BaseMutation):
    mutation_type = "add_none_guard"

    def generate(self, tree, context=None):
        return []

class IncrementIndexMutation(BaseMutation):
    mutation_type = "increment_index"

    def generate(self, tree, context=None):
        return []

MUTATION_REGISTRY = [
    FlipConditionMutation(),
    AddNoneGuardMutation(),
    IncrementIndexMutation(),
]
