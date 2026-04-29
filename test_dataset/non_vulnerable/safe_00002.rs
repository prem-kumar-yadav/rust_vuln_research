// REAL FIXED CODE
// RustSec ID: RUSTSEC-2016-0002 (FIXED)
// Crate: hyper
// Type: unknown (FIXED)
// Extraction Method: repo_search
// GitHub Repo: hyperium/hyper
// Commit: 4492f31
// File: src/proto/h1/dispatch.rs


for _ in 0..16 {
             let _ = self.poll_read(cx)?;
             let _ = self.poll_write(cx)?;
            let _ = self.poll_flush(cx)?;
 
             // This could happen if reading paused before blocking on IO,
             // such as getting to the end of a framed message, but then
             // writing/flushing set the state back to Init. In that case,
             //
             // Using this instead of task::current() and notify() inside
             // the Conn is noticeably faster in pipelined benchmarks.
            if !self.conn.wants_read_again() {
                 //break;
                 return Poll::Ready(Ok(()));
             }
         self.conn.close_write();
     }
 
     fn is_done(&self) -> bool {
         if self.is_closing {
             return true;