// REAL FIXED CODE
// RustSec ID: RUSTSEC-2016-0004 (FIXED)
// Crate: libusb
// Type: unknown (FIXED)
// Extraction Method: repo_search
// GitHub Repo: dcuddeback/libusb-rs
// Commit: 53d6a72
// File: examples/read_device.rs


let args: Vec<String> = std::env::args().collect();
 
     if args.len() < 3 {
        println!("usage: read_device <vendor-id-in-base-10> <product-id-in-base-10>");
         return;
     }