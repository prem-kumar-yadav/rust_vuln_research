// REAL VULNERABLE CODE
// RustSec ID: RUSTSEC-2016-0005
// CVE: N/A
// CWE: N/A
// Crate: rust-crypto
// Type: unknown
// Severity: medium
// Source: https://crates.io/crates/rust-crypto
// Extraction Method: repo_search
// GitHub Repo: DaGenix/rust-crypto
// Commit: cbfa22d
// File: build.rs


// GCC doesn't like some of the assembly that we use on that
                 // platform.
                 cfg.compiler(Path::new("clang"));
            } else {
                 cfg.compiler(Path::new("cc"));
             }
         }