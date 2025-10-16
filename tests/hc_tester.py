from src.io.repo_loader import create_repo
from src.algorithms.hill_climbing import HillClimbing
from src.model.state import State
from src.eval.evaluator import (
    kasus_mahasiswa_bentrok,
    kasus_kapasitas_kurang,
    kasus_dosen_gabisa,
    kasus_dosen_bentrok,
)


def build_state_from_sample():
    repo = create_repo("data/sample_input.json")
    s = State()
    s.initializeDomain(repo)
    return s


def run_variant(variant: str):
    print(f"\n--- Running HillClimbing variant: {variant} ---")
    s = build_state_from_sample()
    algo = HillClimbing(variant=variant)

    final = algo.search(
        s,
        kasus_mahasiswa_bentrok,
        kasus_kapasitas_kurang,
        kasus_dosen_gabisa,
        kasus_dosen_bentrok,
    )

    print(f"Final state value: {final.stateValue}")
    print(f"Number of assignments: {len(final.assignments)}")

    for i, (slot, mk) in enumerate(final.assignments.items()):
        if i >= 10:
            break
        print(f"Slot: {slot[0]} @ ({slot[1].hari}, {slot[1].jam}) -> {mk.kode}")


def main():
    run_variant("steepest")
    run_variant("sideways")
    run_variant("stochastic")
    run_variant("random_restart")


if __name__ == "__main__":
    main()
