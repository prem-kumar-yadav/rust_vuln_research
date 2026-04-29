// REAL FIXED CODE
// RustSec ID: RUSTSEC-2016-0001 (FIXED)
// Crate: openssl
// Type: unknown (FIXED)
// Extraction Method: repo_search
// GitHub Repo: sfackler/rust-openssl
// Commit: ab29b6d
// File: openssl/src/ocsp.rs


#[allow(deprecated)]
                 Some(OcspStatus {
                     status: OcspCertStatus(status),
                    reason: OcspRevokedStatus(reason),
                     revocation_time,
                     this_update: Asn1GeneralizedTimeRef::from_ptr(this_update),
                     next_update: next_update_compat,
 mod tests {
     use super::{
         get_sentinel_max_time, OcspCertId, OcspCertStatus, OcspResponse, OcspResponseStatus,
        OcspRevokedStatus,
     };
     use crate::hash::MessageDigest;
     use crate::x509::X509;
         include_bytes!("../test/ocsp_resp_no_nextupdate.der");
     const OCSP_CA_CERT: &[u8] = include_bytes!("../test/ocsp_ca_cert.der");
     const OCSP_SUBJECT_CERT: &[u8] = include_bytes!("../test/ocsp_subject_cert.der");
    const OCSP_RESPONSE_REVOKED: &[u8] = include_bytes!("../test/ocsp_resp_revoked.der");
 
     #[test]
     fn test_ocsp_no_next_update() {
 
         assert_eq!(status.status, OcspCertStatus::GOOD);
     }

    #[test]
    fn test_ocsp_revoked() {
        let response = OcspResponse::from_der(OCSP_RESPONSE_REVOKED).unwrap();
        assert_eq!(response.status(), OcspResponseStatus::SUCCESSFUL);

        let ca_cert = X509::from_der(OCSP_CA_CERT).unwrap();
        let subject_cert = X509::from_der(OCSP_SUBJECT_CERT).unwrap();
        let basic = response.basic().unwrap();

        let cert_id =
            OcspCertId::from_cert(MessageDigest::sha256(), &subject_cert, &ca_cert).unwrap();

        let status = basic
            .find_status(&cert_id)
            .expect("find_status should find the status");

        assert_eq!(status.status, OcspCertStatus::REVOKED);
        assert_eq!(status.reason, OcspRevokedStatus::STATUS_SUPERSEDED);
    }
 }