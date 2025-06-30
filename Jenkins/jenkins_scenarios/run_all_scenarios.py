#!/usr/bin/env python3

import os

def run_all_scenarios():
    base_dir = os.path.dirname(os.path.abspath(__file__))

    print("\n🚀 CI/CD Chaos Workshop - Run All Jenkins Scenarios")
    print("------------------------------------------------------\n")

    for scenario in sorted(os.listdir(base_dir)):
        scenario_path = os.path.join(base_dir, scenario)

        if os.path.isdir(scenario_path) and scenario.startswith("scenario_"):
            jenkinsfile_path = os.path.join(scenario_path, "Jenkinsfile")
            readme_path = os.path.join(scenario_path, "README.md")

            print(f"➡️ Scenario: {scenario}")

            if os.path.exists(jenkinsfile_path):
                print("✅ Jenkinsfile exists.")
            else:
                print("⚠️ No Jenkinsfile found!")

            if os.path.exists(readme_path):
                print("✅ README.md exists.")
            else:
                print("⚠️ No README.md found!")

            print("\nℹ️ To run this scenario manually:")
            print("   1. Open Jenkins UI.")
            print(f"   2. Create a new Pipeline job for {scenario}.")
            print(f"   3. Copy contents from {jenkinsfile_path}")
            print("   4. Save and run the job.\n")

    print("🎉 All scenarios scanned. Ready for chaos!\n")

if __name__ == "__main__":
    run_all_scenarios()
