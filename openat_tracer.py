// This traces open events for .env files
from bcc import BPF

bpf_code = """
#include <uapi/linux/ptrace.h>
#include <linux/sched.h>

int trace_openat(struct pt_regs *ctx, int dfd, const char __user *filename, int flags, umode_t mode) {
    u32 pid = bpf_get_current_pid_tgid() >> 32;
    char comm[16];
    char fname[256];

    bpf_get_current_comm(&comm, sizeof(comm));
    bpf_probe_read_user_str(&fname, sizeof(fname), filename);

    if (strstr(fname, ".env")) {
        bpf_trace_printk("ENV READ: %s -> %s\\n", comm, fname);
    }
    return 0;
}
"""

b = BPF(text=bpf_code)
b.attach_kprobe(event="__x64_sys_openat", fn_name="trace_openat")
print("Tracing openat... Press Ctrl+C to stop.")
b.trace_print()
