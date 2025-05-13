# 🛠️ Troubleshooting Guide: eBPF Workshop (Rootconf 2025)

This guide will help you debug common runtime issues while running eBPF tracer scripts in this workshop.

---

## ❗ Problem:
```

OSError: \[Errno 16] Device or resource busy: '/sys/kernel/debug/tracing/trace\_pipe'

````

### 🔎 Cause:
- The `/sys/kernel/debug/tracing/trace_pipe` file can only be read by **one process at a time**.
- This happens if:
  - You run multiple tracer scripts simultaneously (e.g., openat.py and connect.py).
  - A previous tracer script is still running in the background.

---

## ✅ Solution: Free Up trace_pipe

### Step 1️⃣: Find who is using trace_pipe
```bash
sudo lsof /sys/kernel/debug/tracing/trace_pipe
````

or

```bash
sudo fuser -v /sys/kernel/debug/tracing/trace_pipe
```

Sample output:

```
COMMAND   PID USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
python3  1234 root    3r   CHR  0,16      0t0 1234 /sys/kernel/debug/tracing/trace_pipe
```

---

### Step 2️⃣: Kill the conflicting process

```bash
sudo kill -9 1234
```

Or use this shortcut:

```bash
sudo fuser -k /sys/kernel/debug/tracing/trace_pipe
```

---

### Step 3️⃣: Re-run your tracer

```bash
sudo python3 connect.py
```

---

## ✅ Pro Tip:

* Always run **one tracer script at a time**.
* To monitor multiple syscalls (e.g., openat + connect), combine them in a single BPF program.

---

## 🧹 Bonus: Clean up environment

Reset everything to clean state:

```bash
sudo pkill -f python3  # Kill all running Python scripts
sudo echo > /sys/kernel/debug/tracing/trace  # Clear trace buffer
```

---

## ✅ Useful Debug Commands:

| Command                                         | Purpose                      |                             |
| ----------------------------------------------- | ---------------------------- | --------------------------- |
| `sudo mount -t debugfs none /sys/kernel/debug`  | Mount debugfs manually       |                             |
| `ls /sys/kernel/debug/tracing`                  | Verify tracefs is accessible |                             |
| `bpftool prog show`                             | List all loaded BPF programs |                             |
| `sudo cat /sys/kernel/debug/tracing/trace_pipe` | View raw trace output        |                             |

---

## ✅ Why This Matters:

* `/sys/kernel/debug/tracing/trace_pipe` is a **global shared pipe**.
* Only one reader allowed at a time.
* This is a **kernel limitation**, not a bug.

---

## ✅ TL;DR:

✅ Run one tracer at a time.
✅ Kill old readers.
✅ Clear trace buffer before rerunning.
