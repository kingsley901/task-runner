"""Main entrypoint for task-runner CLI."""
import argparse
import sys
from runner import TaskRunner
from task import Task


def main():
    parser = argparse.ArgumentParser(description="task-runner: lightweight task scheduler")
    parser.add_argument("--workers", type=int, default=4, help="Max concurrent workers")
    parser.add_argument("--submit", type=str, help="Submit a task by name")
    args = parser.parse_args()

    runner = TaskRunner(max_workers=args.workers)
    runner.start()

    if args.submit:
        task = runner.submit_func(args.submit, args.submit)
        print(f"Submitted: {task.id}")

    print("task-runner started. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping...")
        runner.stop()


if __name__ == "__main__":
    main()
