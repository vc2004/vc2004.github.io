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

## The Modern Workflow: `libbpf`