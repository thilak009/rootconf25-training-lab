from bcc import BPF

bpf_code = """
#include <uapi/linux/ptrace.h>
#include <linux/sched.h>
#include <linux/net.h>

int trace_connect(struct pt_regs *ctx) {
    u32 pid = bpf_get_current_pid_tgid() >> 32;
    char comm[16];
    bpf_get_current_comm(&comm, sizeof(comm));

    bpf_trace_printk("CONNECT: PID %d (%s) is making outbound connection\\n", pid, comm);
    return 0;
}
"""

b = BPF(text=bpf_code)
b.attach_kprobe(event="__x64_sys_connect", fn_name="trace_connect")
print("Tracing connect... Ctrl+C to exit.")
b.trace_print()
