from bcc import BPF

bpf_program = """
#include <uapi/linux/ptrace.h>
#include <linux/sched.h>

// Simple prefix match for /tmp
static inline int starts_with_tmp(const char *filename) {
    return filename[0] == '/' &&
           filename[1] == 't' &&
           filename[2] == 'm' &&
           filename[3] == 'p';
}

TRACEPOINT_PROBE(syscalls, sys_enter_execve) {
    char fname[256];
    char comm[16];
    u32 pid = bpf_get_current_pid_tgid() >> 32;

    bpf_get_current_comm(&comm, sizeof(comm));
    bpf_probe_read_user_str(&fname, sizeof(fname), (void *)args->filename);

    if (starts_with_tmp(fname)) {
        bpf_trace_printk("[ALERT] Exec from /tmp: %s (PID %d)\\n", fname, pid);
    }

    return 0;
}
"""

b = BPF(text=bpf_program)
print("🚀 Tracing execve (process executions from /tmp)... (Ctrl+C to stop)")

try:
    b.trace_print()
except KeyboardInterrupt:
    print("\n🛑 Stopped tracing.")
