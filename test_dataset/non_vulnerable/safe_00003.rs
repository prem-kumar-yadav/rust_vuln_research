// REAL FIXED CODE
// RustSec ID: RUSTSEC-2016-0003 (FIXED)
// Crate: portaudio
// Type: unknown (FIXED)
// Extraction Method: repo_search
// GitHub Repo: RustAudio/rust-portaudio
// Commit: 9b7dfad
// File: src/lib.rs


}
 
 /// Retrieve a textual description of the current PortAudio build.
 pub fn version_text() -> Result<&'static str, ::std::str::Utf8Error> {
     unsafe { ffi::c_str_to_str(ffi::Pa_GetVersionText()) }
 }