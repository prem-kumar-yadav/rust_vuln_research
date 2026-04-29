// REAL VULNERABLE CODE
// RustSec ID: RUSTSEC-2016-0003
// CVE: CVE-2016-10933
// CWE: N/A
// Crate: portaudio
// Type: unknown
// Severity: medium
// Source: https://crates.io/crates/portaudio
// Extraction Method: repo_search
// GitHub Repo: RustAudio/rust-portaudio
// Commit: 9b7dfad
// File: src/lib.rs


}
 
 /// Retrieve a textual description of the current PortAudio build.
///
/// FIXME: This should return a `&'static str`, not a `String`.
 pub fn version_text() -> Result<&'static str, ::std::str::Utf8Error> {
     unsafe { ffi::c_str_to_str(ffi::Pa_GetVersionText()) }
 }