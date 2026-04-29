// REAL VULNERABLE CODE
// RustSec ID: RUSTSEC-2016-0002
// CVE: CVE-2016-10932
// CWE: N/A
// Crate: hyper
// Type: unknown
// Severity: medium
// Source: https://crates.io/crates/hyper
// Extraction Method: repo_search
// GitHub Repo: hyperium/hyper
// Commit: 4492f31
// File: src/proto/h1/dispatch.rs


for _ in 0..16 {
             let _ = self.poll_read(cx)?;
             let _ = self.poll_write(cx)?;
            let conn_ready = self.poll_flush(cx)?.is_ready();
 
            // If we can write more body and the connection is ready, we should
            // write again. If we return `Ready(Ok(())` here, we will yield
            // without a guaranteed wakeup from the write side of the connection.
            // This would lead to a deadlock if we also don't expect reads.
            let wants_write_again = self.can_write_again() && conn_ready;
             // This could happen if reading paused before blocking on IO,
             // such as getting to the end of a framed message, but then
             // writing/flushing set the state back to Init. In that case,
             //
             // Using this instead of task::current() and notify() inside
             // the Conn is noticeably faster in pipelined benchmarks.
            let wants_read_again = self.conn.wants_read_again();
            // If we cannot write or read again, we yield and rely on the
            // wakeup from the connection futures.
            if !(wants_write_again || wants_read_again) {
                 //break;
                 return Poll::Ready(Ok(()));
             }
         self.conn.close_write();
     }
 
    /// If there is pending data in body_rx, we can make progress writing if the connection is ready.
    fn can_write_again(&mut self) -> bool {
        self.body_rx.is_some()
    }

     fn is_done(&self) -> bool {
         if self.is_closing {
             return true;