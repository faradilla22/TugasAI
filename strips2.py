class Action:
    def _init_(self, name, preconditions, effects):
        self.name = name
        self.preconditions = preconditions
        self.effects = effects

class State:
    def _init_(self, grades):
        self.grades = grades

class Planner:
    def _init_(self, initial_state, goal_state, actions):
        self.initial_state = initial_state
        self.goal_state = goal_state
        self.actions = actions

    def plan(self):
        plan = []
        current_state = self.initial_state

        while not self.goal_satisfied(current_state):
            applicable_actions = self.get_applicable_actions(current_state)
            chosen_action = self.choose_action(applicable_actions)
            plan.append(chosen_action)
            current_state = self.apply_action(current_state, chosen_action)

        return plan

    def goal_satisfied(self, state):
        for subject, grade in state.grades.items():
            if grade < self.goal_state.grades[subject]:
                return False
        return True

    def get_applicable_actions(self, state):
        applicable_actions = []
        for action in self.actions:
            if all(precondition in state.grades.items() for precondition in action.preconditions.items()):
                applicable_actions.append(action)
        return applicable_actions

    def choose_action(self, applicable_actions):

        return applicable_actions[0]

    def apply_action(self, state, action):
        new_state = State(state.grades.copy())
        for effect, value in action.effects.items():
            new_state.grades[effect] += value
        return new_state

actions = [
    Action(
        "Selamat anda memenuhi syarat",
        {"CV": 55},
        {"CV": 45}
    ),
    Action(
        "Mandapatkan Pengalaman",
        {"CV": 45},
        {"CV": 10}
    ),
    Action(
        "Mendapatkan Skill yang cukup",
        {"CV": 40},
        {"CV": 15}
    ),
  Action(
        "Mendapatkan Pendidikan yang Cukup",
        {"CV": 25},
        {"CV": 30}
    ),
    Action(
        "Memdapatkan Pengalaman yang cukup",
        {"CV": 35},
        {"CV": 20}
    ),
    Action(
        "Mendapatkan Skill yang cukup",
        {"CV": 30},
        {"CV": 5}
    ),
    Action(
        "Mendapatkan Skill yang Cukup",
        {"CV": 20},
        {"CV": 35}
    ),
    Action(
        "Mendapatkan Pendidikan yang Cukup",
        {"CV": 10},
        {"CV": 10}
    ),
    Action(
        "Mendapatkan Pendidikan yang Cukup",
        {"CV": 15},
        {"CV": 12}
    ),
    Action(
        "Mendapatkan Pengalaman yang cukup",
        {"CV": 27},
        {"CV": 28}
    ),
    Action(
        "Mendapatkan Pendidikan,Pengalaman dan skill yang cukup",
        {"CV": 0},
        {"CV": 55}
    )
  
]

# Define initial state 
#Kasih skor cvnyo contohnyo 50

initial_state = State({"CV":10})

# Define goal state
goal_state = State({"CV": 100})

# Create planner
planner = Planner(initial_state, goal_state, actions)

# Plan and print
plan = planner.plan()
print("Rencana agar bisa diterima:")
for action in plan:
    print(action.name)

"""
pend =30
skill = 15
if int pengalaman = 10

sma
tanpa skill
pengalaman


"""