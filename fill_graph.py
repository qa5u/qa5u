#!/usr/bin/env python3
import subprocess
import random
import time
import os
import sys
from datetime import datetime, timedelta

random.seed(42)

today = datetime(2026, 10, 21)
start = today - timedelta(days=21)

all_days = [start + timedelta(days=d) for d in range(22)]
commit_days = sorted(random.sample(all_days, 7))

print(f"Total days in range: {len(all_days)}")
print(f"Days with commits: {len(commit_days)}")
print()

success = 0
errors = 0

for day in commit_days:
    day_str = day.strftime("%Y-%m-%d")
    num_commits = random.randint(1, 3)
    print(f"{day_str}: {num_commits} commit(s)")

    for i in range(num_commits):
        hour = random.randint(8, 22)
        minute = random.randint(0, 59)
        second = random.randint(0, 59)
        commit_time = day.replace(hour=hour, minute=minute, second=second)
        timestamp = commit_time.strftime("%Y-%m-%dT%H:%M:%S+03:00")

        env = dict(os.environ)
        env["GIT_COMMITTER_NAME"] = "qa5u"
        env["GIT_COMMITTER_EMAIL"] = "qa5u@users.noreply.github.com"
        env["GIT_COMMITTER_DATE"] = timestamp
        env["GIT_AUTHOR_NAME"] = "qa5u"
        env["GIT_AUTHOR_EMAIL"] = "qa5u@users.noreply.github.com"
        env["GIT_AUTHOR_DATE"] = timestamp

        msg = f"Commit from {day_str}"
        result = subprocess.run(
            ["git", "commit", "--allow-empty", "-m", msg],
            capture_output=True,
            text=True,
            env=env,
        )
        if result.returncode != 0:
            print(f"  ERROR: {result.stderr.strip()}")
            errors += 1
        else:
            sha = result.stdout.strip().split()[-1] if result.stdout.strip() else "?"
            print(f"    {sha[:8]} @ {commit_time.strftime('%H:%M')}")
            success += 1
        time.sleep(0.2)

print()
print(f"Done: {success} commits created, {errors} errors")
sys.exit(errors)
