// REAL VULNERABLE CODE
// RustSec ID: RUSTSEC-2016-0004
// CVE: N/A
// CWE: N/A
// Crate: libusb
// Type: unknown
// Severity: medium
// Source: https://crates.io/crates/libusb
// Extraction Method: repo_search
// GitHub Repo: dcuddeback/libusb-rs
// Commit: 53d6a72
// File: examples/read_device.rs


let args: Vec<String> = std::env::args().collect();
 
     if args.len() < 3 {
        println!("usage: show_device <vendor-id> <product-id>");
         return;
     }