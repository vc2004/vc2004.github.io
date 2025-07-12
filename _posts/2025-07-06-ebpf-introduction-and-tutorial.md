---
layout: blog
title: "eBPF Deep Dive: Architecture, Development, and a Practical Tutorial"
date: 2025-07-06 18:30:00 +0800
categories: [Technology, eBPF, Linux, Kernel, Deep Dive]
---

Our previous post introduced eBPF as a powerful tool for observing the Linux kernel. Now, it's time for a deep dive. We'll move beyond high-level tools and explore the architecture, development process, and core components that make eBPF a game-changer for cloud-native infrastructure, security, and networking.

## The eBPF Core Architecture

Understanding how eBPF works requires looking at the journey of an eBPF program from source code to execution.

1.  **Writing the Code**: Developers write eBPF programs in a restricted subset of C. A separate user-space program is also written to load and interact with the eBPF program.

2.  **Compilation**: A compiler toolchain, typically **Clang/LLVM**, compiles the C code into eBPF bytecode—a special instruction set understood by the kernel.

3.  **Loading**: The user-space program uses the `bpf()` system call to load the eBPF bytecode into the kernel.

4.  **Verification**: This is the most critical step. The **Verifier** statically analyzes the bytecode to ensure it's safe to run. It checks for:
    *   **No Unbounded Loops**: Prevents kernel lock-ups.
    *   **Valid Memory Access**: The program can only access its own stack and data from eBPF maps.
    *   **Finite Execution**: The program must be guaranteed to finish.
    If any check fails, the kernel refuses to load the program.

5.  **JIT Compilation**: Once verified, the **Just-In-Time (JIT) compiler** translates the eBPF bytecode into native machine code for the host CPU. This makes execution extremely fast, often near native speed.

6.  **Attachment**: The program is attached to a specific **hook** (e.g., a system call, a network event).

7.  **Execution**: When the hooked event occurs, the kernel executes the compiled eBPF program.

![eBPF Architecture](https://raw.githubusercontent.com/cilium/cilium/main/Documentation/images/ebpf_architecture.png)
*(Image credit: Cilium Project)*

## Key Components in Detail

### Program Types & Hooks

eBPF is versatile because it can attach to many different kernel hooks. The program type determines which hooks are available and what the program is allowed to do.

| Program Type      | Hook Point                      | Use Case                                               |
| ----------------- | ------------------------------- | ------------------------------------------------------ |
| `kprobe`/`kretprobe` | Entry/Exit of any kernel function | Dynamic tracing, performance analysis, debugging       |
| `tracepoint`      | Static kernel tracepoints       | Stable, low-overhead tracing of kernel events          |
| `XDP`             | Network driver receive path     | High-performance packet processing, DDoS mitigation    |
| `TC` (Traffic Control) | Kernel network stack (qdiscs)   | Sophisticated packet filtering, routing, and mangling  |
| `LSM` (Linux Security) | Security-related kernel hooks   | Implementing mandatory access control, security auditing |

### eBPF Maps

Maps are the primary way eBPF programs store state and communicate. They are efficient key/value stores accessible from both the eBPF program (in-kernel) and the user-space control program.

Common map types include:
*   `BPF_MAP_TYPE_HASH`: A generic hash map.
*   `BPF_MAP_TYPE_ARRAY`: A simple array, often used for counters.
*   `BPF_MAP_TYPE_PERF_EVENT_ARRAY`: A specialized map for sending data to user space via the high-performance perf buffer.
*   `BPF_MAP_TYPE_RINGBUF`: A more modern and flexible alternative to the perf buffer.

### Helper Functions

eBPF programs cannot call arbitrary kernel functions. Instead, the kernel provides a stable set of **helper functions**. These are well-defined APIs for tasks like:
*   `bpf_map_lookup_elem()`: Find an element in a map.
*   `bpf_map_update_elem()`: Update an element in a map.
*   `bpf_get_current_pid_tgid()`: Get the ID of the current process.
*   `bpf_ktime_get_ns()`: Get the current kernel time.

## The Modern Workflow: `libbpf` and CO-RE

Early eBPF development was painful. Developers had to manually rewrite parts of their code to match different kernel versions. The modern solution is **`libbpf`** combined with **CO-RE (Compile Once - Run Everywhere)**.

*   **BTF (BPF Type Format)**: This is debugging information embedded in the kernel that describes its internal data structures. `libbpf` uses BTF to understand the memory layout of structs on the target kernel at runtime.
*   **`libbpf`**: A C library that has become the standard for writing eBPF applications. It automatically handles loading, verifying, and attaching programs. It also performs CO-RE relocations, adjusting the eBPF bytecode on the fly to match the running kernel.
*   **Skeletons**: `libbpf` can generate a special header file (a "skeleton") from your eBPF C code. This skeleton provides a clean API for your user-space program to interact with the eBPF program and its maps.

## Practical Tutorial: Counting `execve` with `libbpf`

Let's build a simple eBPF application that counts every `execve` system call on the system.

### Prerequisites

You'll need `clang`, `llvm`, `libbpf-dev` (or `libbpf-devel`), and the kernel headers.

```bash
# Ubuntu/Debian
sudo apt-get install -y clang llvm libbpf-dev linux-headers-$(uname -r)

# Fedora/CentOS
sudo dnf install -y clang llvm libbpf-devel kernel-devel
```

### Step 1: The eBPF Kernel Code (`counter.bpf.c`)

This code will run inside the kernel.

```c
#include <vmlinux.h>
#include <bpf/bpf_helpers.h>

// Define a simple array map to hold our counter
struct {
    __uint(type, BPF_MAP_TYPE_ARRAY);
    __uint(max_entries, 1);
    __type(key, u32);
    __type(value, u64);
} exec_count_map SEC(".maps");

// Attach to the tracepoint for the execve system call entry
SEC("tp/syscalls/sys_enter_execve")
int handle_execve(struct trace_event_raw_sys_enter *ctx) {
    u32 key = 0;
    u64 *count;

    count = bpf_map_lookup_elem(&exec_count_map, &key);
    if (count) {
        __sync_fetch_and_add(count, 1);
    }

    return 0;
}

// Required license for eBPF programs
char LICENSE[] SEC("license") = "GPL";
```

### Step 2: The User-space Loader (`counter.c`)

This C program loads and interacts with our eBPF code.

```c
#include <stdio.h>
#include <unistd.h>
#include <bpf/libbpf.h>
#include "counter.skel.h" // Generated by libbpf

int main(int argc, char **argv) {
    struct counter_bpf *skel;
    int err;
    u32 key = 0;
    u64 count;

    // Open, load, and verify the BPF application
    skel = counter_bpf__open_and_load();
    if (!skel) {
        fprintf(stderr, "Failed to open BPF skeleton\n");
        return 1;
    }

    // Attach tracepoint handler
    err = counter_bpf__attach(skel);
    if (err) {
        fprintf(stderr, "Failed to attach BPF skeleton\n");
        goto cleanup;
    }

    printf("Counting execve() syscalls... Press Ctrl-C to exit.\n");

    // Main loop
    while (true) {
        sleep(2);
        err = bpf_map_lookup_elem(bpf_map__fd(skel->maps.exec_count_map), &key, &count);
        if (err == 0) {
            printf("execve() calls: %llu\n", count);
        } else {
            fprintf(stderr, "Failed to read map: %d\n", err);
        }
    }

cleanup:
    counter_bpf__destroy(skel);
    return -err;
}
```

### Step 3: Compile and Run

1.  **Compile the eBPF code into an object file:**
    ```bash
    clang -g -O2 -target bpf -c counter.bpf.c -o counter.bpf.o
    ```

2.  **Generate the BPF skeleton header:**
    ```bash
    bpftool gen skeleton counter.bpf.o > counter.skel.h
    ```

3.  **Compile the user-space application:**
    ```bash
    clang -g -O2 -c counter.c -o counter.o
    clang counter.o -lbpf -o counter
    ```

4.  **Run it!**
    ```bash
    sudo ./counter
    ```

Now, if you open another terminal and run some commands (`ls`, `whoami`, etc.), you will see the counter in the first terminal increase.

## Conclusion

eBPF is more than just a tool; it's a fundamental shift in how we interact with the operating system. By providing a safe, performant, and programmable interface deep within the kernel, eBPF has unlocked a new wave of innovation. While the learning curve can be steep, the power and flexibility it offers are unmatched. This deep dive provides the foundational knowledge you need to start writing your own eBPF-powered applications and truly harness the power of the Linux kernel.

For further reading, check out the [eBPF.io documentation](https://ebpf.io/) and the [libbpf GitHub repository](https://github.com/libbpf/libbpf).