// REAL FIXED CODE
// RustSec ID: RUSTSEC-2016-0005 (FIXED)
// Crate: rust-crypto
// Type: unknown (FIXED)
// Extraction Method: repo_search
// GitHub Repo: DaGenix/rust-crypto
// Commit: cbfa22d
// File: build.rs


// GCC doesn't like some of the assembly that we use on that
                 // platform.
                 cfg.compiler(Path::new("clang"));
            } else if target == host {
                 cfg.compiler(Path::new("cc"));
             }
         }