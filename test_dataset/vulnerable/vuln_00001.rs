// REAL VULNERABLE CODE
// RustSec ID: RUSTSEC-2016-0001
// CVE: CVE-2016-10931
// CWE: N/A
// Crate: openssl
// Type: unknown
// Severity: medium
// Source: https://crates.io/crates/openssl
// Extraction Method: repo_search
// GitHub Repo: sfackler/rust-openssl
// Commit: ab29b6d
// File: openssl/src/ocsp.rs


#[allow(deprecated)]
                 Some(OcspStatus {
                     status: OcspCertStatus(status),
                    reason: OcspRevokedStatus(status),
                     revocation_time,
                     this_update: Asn1GeneralizedTimeRef::from_ptr(this_update),
                     next_update: next_update_compat,
 mod tests {
     use super::{
         get_sentinel_max_time, OcspCertId, OcspCertStatus, OcspResponse, OcspResponseStatus,
     };
     use crate::hash::MessageDigest;
     use crate::x509::X509;
         include_bytes!("../test/ocsp_resp_no_nextupdate.der");
     const OCSP_CA_CERT: &[u8] = include_bytes!("../test/ocsp_ca_cert.der");
     const OCSP_SUBJECT_CERT: &[u8] = include_bytes!("../test/ocsp_subject_cert.der");
 
     #[test]
     fn test_ocsp_no_next_update() {
 
         assert_eq!(status.status, OcspCertStatus::GOOD);
     }
 }