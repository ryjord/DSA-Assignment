from utils import load_test_case;
from algo_ai import run_ai_solution;
from naive import run_naive_solution;
from algo_optimised import run_optimised_solution;
import pydash as _;
def main():
  data = load_test_case('../data/test_case_1.json');
  if not _.is_none(data):
    dist_matrix = data['distance_matrix'];
    demands = data['demands'];
    capacity = data['vehicle_capacity'];
    print("Executing AI Solution...");
    ai_result = run_ai_solution(dist_matrix, demands, capacity);
    print(f"AI Result: { ai_result }");
if __name__ == "__main__":
  main();