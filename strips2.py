import heapq
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

class Operator:
    def __init__(self, name, preconditions, effects, cost):
        self.name = name
        self.preconditions = preconditions
        self.effects = effects
        self.cost = cost

class State:
    def __init__(self, conditions):
        self.conditions = set(conditions)

    def __eq__(self, other):
        return self.conditions == other.conditions

    def __hash__(self):
        return hash(frozenset(self.conditions))

class Planner:
    def __init__(self, operators, initial_state, goal_state):
        self.operators = operators
        self.initial_state = initial_state
        self.goal_state = goal_state

    def plan(self):
        open_set = [(0, self.initial_state, [])]  # (cost, state, actions)
        closed_set = set()

        while open_set:
            cost, current_state, actions = heapq.heappop(open_set)

            if current_state in closed_set:
                continue

            if current_state == self.goal_state:
                return actions

            closed_set.add(current_state)

            for op in self.operators:
                if self.applicable(op, current_state):
                    new_state = self.apply(op, current_state)
                    new_cost = cost + op.cost
                    new_actions = actions + [(op.name, new_cost)]  # Tambahan: menyimpan biaya setiap langkah
                    heapq.heappush(open_set, (new_cost, new_state, new_actions))

        return None

    def applicable(self, op, state):
        return all(condition in state.conditions for condition in op.preconditions)

    def apply(self, op, state):
        new_state = state.conditions.copy()
        new_state.difference_update(op.effects)
        new_state.update(op.preconditions)
        return State(new_state)

def format_plan(plan):
    formatted_plan = []
    total_cost = 0  # Tambahan: total biaya
    for step, (action, cost) in enumerate(plan, 1):
        formatted_plan.append(f"Langkah {step}: {action}, Biaya: {cost}")
        total_cost += cost
    formatted_plan.append(f"Total Biaya: {total_cost}")  # Tambahan: total biaya
    return formatted_plan

def main():
    # Definisikan operator dengan biaya
    operators = [
        Operator("selesaikan_gelar", {"belum_gelar"}, {"gelar"}, 4),
        Operator("ikuti_kursus", {"gelar", "belum_kursus"}, {"kursus"}, 2),
        Operator("dapatkan_pengalaman", {"gelar", "kursus", "belum_pengalaman"}, {"pengalaman"}, 3),
        Operator("cari_pekerjaan", {"gelar", "kursus", "pengalaman", "belum_pekerjaan"}, {"pekerjaan"}, 5)
    ]

    # Definisikan state awal dan tujuan
    initial_state = State(["belum_gelar", "belum_kursus", "belum_pengalaman", "belum_pekerjaan"])
    goal_state = State(["gelar", "kursus", "pengalaman", "pekerjaan"])

    # Inisialisasi planner dan jalankan perencanaan
    planner = Planner(operators, initial_state, goal_state)
    plan = planner.plan()

    # Output hasil perencanaan
    if plan:
        print("Langkah-langkah perencanaan:")
        formatted_plan = format_plan(plan)
        for step in formatted_plan:
            print(step)
    else:
        print("Tidak ada rencana yang ditemukan untuk mencapai tujuan.")

    # Machine learning untuk rekomendasi karir
    # Data historis (contoh saja, seharusnya lebih lengkap)
    data = [
        ["Pemrograman", "Jaringan", "Keamanan", "Pengembang Perangkat Lunak"],
        ["Pemrograman", "Basis Data", "Analisis Data", "Data Scientist"],
        ["Desain", "Pemodelan", "Animasi", "Desainer Grafis"]
    ]
    X = [d[:-1] for d in data]
    y = [d[-1] for d in data]

    # Label encoding
    label_encoders = [LabelEncoder() for _ in range(len(X[0]))]
    for i in range(len(label_encoders)):
        X[:, i] = label_encoders[i].fit_transform(X[:, i])

    # Split data untuk training dan testing
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Model machine learning
    model = MLPClassifier(hidden_layer_sizes=(10, 10), max_iter=1000, random_state=42)
    model.fit(X_train, y_train)

    # Prediksi karir
    minat = input("Masukkan minat Anda (Pemrograman, Jaringan, Keamanan, Desain, dll.): ")
    kemampuan = input("Masukkan kemampuan Anda (Basis Data, Animasi, Pemodelan, dll.): ")
    preferensi = input("Masukkan preferensi Anda (Pengembang Perangkat Lunak, Data Scientist, Desainer Grafis, dll.): ")

    input_data = [minat, kemampuan, preferensi]
    for i in range(len(label_encoders)):
        input_data[i] = label_encoders[i].transform([input_data[i]])[0]

    prediction = model.predict([input_data])
    print(f"Rekomendasi karir berdasarkan informasi yang Anda berikan: {prediction[0]}")

if __name__ == "__main__":
    main()
